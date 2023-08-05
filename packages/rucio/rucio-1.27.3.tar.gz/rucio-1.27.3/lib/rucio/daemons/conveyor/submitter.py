# -*- coding: utf-8 -*-
# Copyright 2013-2021 CERN
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors:
# - Mario Lassnig <mario.lassnig@cern.ch>, 2013-2015
# - Cedric Serfon <cedric.serfon@cern.ch>, 2013-2019
# - Ralph Vigne <ralph.vigne@cern.ch>, 2013
# - Vincent Garonne <vincent.garonne@cern.ch>, 2014-2018
# - Martin Barisits <martin.barisits@cern.ch>, 2014-2021
# - Wen Guan <wen.guan@cern.ch>, 2014-2016
# - Tomáš Kouba <tomas.kouba@cern.ch>, 2014
# - Joaquín Bogado <jbogado@linti.unlp.edu.ar>, 2016
# - dciangot <diego.ciangottini@cern.ch>, 2018
# - Hannes Hansen <hannes.jakob.hansen@cern.ch>, 2018-2019
# - Matt Snyder <msnyder@bnl.gov>, 2019-2021
# - Brandon White <bjwhite@fnal.gov>, 2019
# - Thomas Beermann <thomas.beermann@cern.ch>, 2020-2021
# - Nick Smith <nick.smith@cern.ch>, 2020-2021
# - James Perry <j.perry@epcc.ed.ac.uk>, 2020
# - Patrick Austin <patrick.austin@stfc.ac.uk>, 2020
# - Benedikt Ziemons <benedikt.ziemons@cern.ch>, 2020-2021
# - Radu Carpa <radu.carpa@cern.ch>, 2021

"""
Conveyor transfer submitter is a daemon to manage non-tape file transfers.
"""

from __future__ import division

import logging
import threading
import time
from collections import defaultdict

from six.moves.configparser import NoOptionError

import rucio.db.sqla.util
from rucio.common import exception
from rucio.common.config import config_get, config_get_bool, config_get_int
from rucio.common.logging import setup_logging
from rucio.common.schema import get_schema_value
from rucio.common.utils import PriorityQueue
from rucio.core import transfer as transfer_core
from rucio.core.monitor import MultiCounter, record_timer
from rucio.daemons.conveyor.common import submit_transfer, get_conveyor_rses, HeartbeatHandler
from rucio.db.sqla.constants import RequestType
from rucio.transfertool.fts3 import FTS3Transfertool
from rucio.transfertool.globus import GlobusTransferTool
from rucio.transfertool.mock import MockTransfertool

graceful_stop = threading.Event()

TRANSFER_TOOL = config_get('conveyor', 'transfertool', False, None)  # NOTE: This should eventually be completely removed, as it can be fetched from the request
FILTER_TRANSFERTOOL = config_get('conveyor', 'filter_transfertool', False, None)  # NOTE: TRANSFERTOOL to filter requests on
TRANSFER_TYPE = config_get('conveyor', 'transfertype', False, 'single')

GET_TRANSFERS_COUNTER = MultiCounter(prom='rucio_daemons_conveyor_submitter_get_transfers', statsd='daemons.conveyor.transfer_submitter.get_transfers',
                                     documentation='Number of transfers retrieved')

TRANSFERTOOL_CLASSES_BY_NAME = {
    'fts3': FTS3Transfertool,
    'globus': GlobusTransferTool,
    'mock': MockTransfertool,
}


def submitter(once=False, rses=None, partition_wait_time=10,
              bulk=100, group_bulk=1, group_policy='rule', source_strategy=None,
              activities=None, sleep_time=600, max_sources=4, archive_timeout_override=None,
              filter_transfertool=FILTER_TRANSFERTOOL, transfertool=TRANSFER_TOOL,
              transfertype=TRANSFER_TYPE, ignore_availability=False):
    """
    Main loop to submit a new transfer primitive to a transfertool.
    """

    try:
        partition_hash_var = config_get('conveyor', 'partition_hash_var')
    except NoOptionError:
        partition_hash_var = None
    try:
        scheme = config_get('conveyor', 'scheme')
    except NoOptionError:
        scheme = None
    try:
        failover_scheme = config_get('conveyor', 'failover_scheme')
    except NoOptionError:
        failover_scheme = None
    try:
        timeout = config_get('conveyor', 'submit_timeout')
        timeout = float(timeout)
    except NoOptionError:
        timeout = None

    try:
        bring_online = config_get_int('conveyor', 'bring_online')
    except NoOptionError:
        bring_online = 43200

    try:
        max_time_in_queue = {}
        timelife_conf = config_get('conveyor', 'max_time_in_queue')
        timelife_confs = timelife_conf.split(",")
        for conf in timelife_confs:
            act, timelife = conf.split(":")
            max_time_in_queue[act.strip()] = int(timelife.strip())
    except NoOptionError:
        max_time_in_queue = {}

    if 'default' not in max_time_in_queue:
        max_time_in_queue['default'] = 168
    logging.debug("Maximum time in queue for different activities: %s", max_time_in_queue)

    activity_next_exe_time = defaultdict(time.time)
    logger_prefix = executable = "conveyor-submitter"
    if activities:
        activities.sort()
        executable += '--activities ' + str(activities)
    if filter_transfertool:
        executable += ' --filter-transfertool ' + filter_transfertool

    if activities is None:
        activities = [None]
    if rses:
        rse_ids = [rse['id'] for rse in rses]
    else:
        rse_ids = None

    with HeartbeatHandler(executable=executable, logger_prefix=logger_prefix) as heartbeat_handler:
        logger = heartbeat_handler.logger
        logger(logging.INFO, 'Submitter starting with timeout %s', timeout)

        if partition_wait_time:
            graceful_stop.wait(partition_wait_time)

        activity_next_exe_time = PriorityQueue()
        for activity in activities:
            activity_next_exe_time[activity] = time.time()

        while not graceful_stop.is_set() and activity_next_exe_time:
            try:
                time_to_sleep = 0
                if once:
                    activity = activity_next_exe_time.pop()
                else:
                    activity = activity_next_exe_time.top()
                    time_to_sleep = activity_next_exe_time[activity] - time.time()
                    activity_next_exe_time[activity] = time.time() + 1
                if time_to_sleep > 0:
                    logger(logging.DEBUG, 'Switching to activity %s and sleeping %s seconds', activity, time_to_sleep)
                    graceful_stop.wait(time_to_sleep)
                else:
                    logger(logging.DEBUG, 'Switching to activity %s', activity)

                heart_beat, logger = heartbeat_handler.live(older_than=3600)

                start_time = time.time()

                transfertool_kwargs = {
                    FTS3Transfertool: {
                        'group_policy': group_policy,
                        'group_bulk': group_bulk,
                        'source_strategy': source_strategy,
                        'max_time_in_queue': max_time_in_queue,
                        'bring_online': bring_online,
                        'default_lifetime': 172800,
                        'archive_timeout_override': archive_timeout_override,
                    },
                    GlobusTransferTool: {
                        'group_policy': transfertype,
                        'group_bulk': group_bulk,
                    },
                }
                transfers = transfer_core.next_transfers_to_submit(
                    total_workers=heart_beat['nr_threads'],
                    worker_number=heart_beat['assign_thread'],
                    partition_hash_var=partition_hash_var,
                    failover_schemes=failover_scheme,
                    limit=bulk,
                    activity=activity,
                    rses=rse_ids,
                    schemes=scheme,
                    filter_transfertool=filter_transfertool,
                    transfertools_by_name={transfertool: TRANSFERTOOL_CLASSES_BY_NAME[transfertool]},
                    older_than=None,
                    request_type=RequestType.TRANSFER,
                    ignore_availability=ignore_availability,
                    logger=logger,
                )
                total_transfers = len(list(hop for paths in transfers.values() for path in paths for hop in path))

                record_timer('daemons.conveyor.transfer_submitter.get_transfers.per_transfer', (time.time() - start_time) * 1000 / (total_transfers or 1))
                GET_TRANSFERS_COUNTER.inc(total_transfers)
                record_timer('daemons.conveyor.transfer_submitter.get_transfers.transfers', total_transfers)
                logger(logging.INFO, '%sGot %s transfers for %s in %s seconds',
                       'Slept %s seconds, then ' % time_to_sleep if time_to_sleep > 0 else '',
                       total_transfers, activity, time.time() - start_time)

                for builder, transfer_paths in transfers.items():
                    transfertool_obj = builder.make_transfertool(logger=logger, **transfertool_kwargs.get(builder.transfertool_class, {}))
                    start_time = time.time()
                    logger(logging.DEBUG, 'Starting to group transfers for %s (%s)', activity, transfertool_obj)
                    grouped_jobs = transfertool_obj.group_into_submit_jobs(transfer_paths)
                    record_timer('daemons.conveyor.transfer_submitter.bulk_group_transfer', (time.time() - start_time) * 1000 / (len(transfer_paths) or 1))

                    logger(logging.DEBUG, 'Starting to submit transfers for %s (%s)', activity, transfertool_obj)
                    for job in grouped_jobs:
                        logger(logging.DEBUG, 'submitjob: transfers=%s, job_params=%s' % ([str(t) for t in job['transfers']], job['job_params']))
                        submit_transfer(transfertool_obj=transfertool_obj, transfers=job['transfers'], job_params=job['job_params'], submitter='transfer_submitter',
                                        timeout=timeout, logger=logger)

                if not once and total_transfers < group_bulk:
                    logger(logging.DEBUG, 'Only %s transfers for %s which is less than group bulk %s, sleep %s seconds', total_transfers, activity, group_bulk, sleep_time)
                    activity_next_exe_time[activity] = time.time() + sleep_time

            except Exception:
                logger(logging.CRITICAL, 'Exception', exc_info=True)
                if once:
                    raise


def stop(signum=None, frame=None):
    """
    Graceful exit.
    """
    graceful_stop.set()


def run(once=False, group_bulk=1, group_policy='rule', mock=False,
        rses=None, include_rses=None, exclude_rses=None, vos=None, bulk=100, source_strategy=None,
        activities=None, exclude_activities=None, ignore_availability=False, sleep_time=600, max_sources=4,
        archive_timeout_override=None, total_threads=1):
    """
    Starts up the conveyer threads.
    """
    setup_logging()

    if rucio.db.sqla.util.is_old_db():
        raise exception.DatabaseException('Database was not updated, daemon won\'t start')

    multi_vo = config_get_bool('common', 'multi_vo', raise_exception=False, default=False)
    working_rses = None
    if rses or include_rses or exclude_rses:
        working_rses = get_conveyor_rses(rses, include_rses, exclude_rses, vos)
        logging.info("RSE selection: RSEs: %s, Include: %s, Exclude: %s", rses, include_rses, exclude_rses)
    elif multi_vo:
        working_rses = get_conveyor_rses(rses, include_rses, exclude_rses, vos)
        logging.info("RSE selection: automatic for relevant VOs")
    else:
        logging.info("RSE selection: automatic")

    logging.info('starting submitter threads')

    if exclude_activities:
        if not activities:
            if not multi_vo:
                vos = ['def']
            if vos and len(vos) == 1:
                activities = get_schema_value('ACTIVITY', vos[0])
            elif vos and len(vos) > 1:
                logging.warning('Cannot get activity list from schema when multiple VOs given, either provide `activities` argument or run on a single VO')
                activities = [None]
            else:
                logging.warning('Cannot get activity list from schema when no VO given, either provide `activities` argument or `vos` with a single entry')
                activities = [None]

        for activity in exclude_activities:
            if activity in activities:
                activities.remove(activity)

    threads = [threading.Thread(target=submitter, kwargs={'once': once,
                                                          'rses': working_rses,
                                                          'bulk': bulk,
                                                          'group_bulk': group_bulk,
                                                          'group_policy': group_policy,
                                                          'activities': activities,
                                                          'ignore_availability': ignore_availability,
                                                          'sleep_time': sleep_time,
                                                          'max_sources': max_sources,
                                                          'source_strategy': source_strategy,
                                                          'archive_timeout_override': archive_timeout_override}) for _ in range(0, total_threads)]

    [thread.start() for thread in threads]

    logging.info('waiting for interrupts')

    # Interruptible joins require a timeout.
    while threads:
        threads = [thread.join(timeout=3.14) for thread in threads if thread and thread.is_alive()]
