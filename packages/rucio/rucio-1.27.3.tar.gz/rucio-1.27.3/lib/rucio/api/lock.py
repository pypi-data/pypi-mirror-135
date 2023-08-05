# -*- coding: utf-8 -*-
# Copyright 2014-2021 CERN
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
# - Martin Barisits <martin.barisits@cern.ch>, 2014-2021
# - Hannes Hansen <hannes.jakob.hansen@cern.ch>, 2018
# - Andrew Lister <andrew.lister@stfc.ac.uk>, 2019
# - Eli Chadwick <eli.chadwick@stfc.ac.uk>, 2020

import logging

from rucio.common.types import InternalScope
from rucio.common.utils import api_update_return_dict
from rucio.core import lock
from rucio.core.rse import get_rse_id
from rucio.db.sqla.constants import DIDType


LOGGER = logging.getLogger('lock')
LOGGER.setLevel(logging.DEBUG)


def get_dataset_locks(scope, name, vo='def'):
    """
    Get the dataset locks of a dataset.

    :param scope:          Scope of the dataset.
    :param name:           Name of the dataset.
    :param vo:             The VO to act on.
    :return:               List of dicts {'rse_id': ..., 'state': ...}
    """

    scope = InternalScope(scope, vo=vo)

    locks = lock.get_dataset_locks(scope=scope, name=name)

    for lock_object in locks:
        yield api_update_return_dict(lock_object)


def get_dataset_locks_bulk(dids, vo='def'):
    """
    Get the dataset locks for multiple datasets or containers.

    :param dids:            List of dataset or container DIDs as dictionaries {"scope":..., "name":..., "type":...}
                            "type" is optional. If present, will be either DIDType.DATASET or DIDType.CONTAINER,
                            or string "dataset" or "container"
    :param vo:              The VO to act on.
    :return:                Generator of dicts describing found locks {'rse_id': ..., 'state': ...}. Duplicates are removed
    """

    if vo is None:
        vo = "def"

    dids_converted = []
    for did_in in dids:
        did = did_in.copy()
        if isinstance(did.get("type"), str):
            # convert DID type
            try:
                did["type"] = {
                    "dataset": DIDType.DATASET,
                    "container": DIDType.CONTAINER
                }[did["type"]]
            except KeyError:
                raise ValueError("Unknown DID type %(type)s" % did)
        if isinstance(did["scope"], str):
            did["scope"] = InternalScope(did["scope"], vo=vo)
        dids_converted.append(did)

    seen = set()
    for lock_info in lock.get_dataset_locks_bulk(dids_converted):
        # filter duplicates - same scope, name, rse_id, rule_id
        scope_str = str(lock_info["scope"])
        key = (scope_str, lock_info["name"], lock_info["rse_id"], lock_info["rule_id"])
        if key not in seen:
            seen.add(key)
            yield lock_info


def get_dataset_locks_by_rse(rse, vo='def'):
    """
    Get the dataset locks of an RSE.

    :param rse:            RSE name.
    :param vo:             The VO to act on.
    :return:               List of dicts {'rse_id': ..., 'state': ...}
    """

    rse_id = get_rse_id(rse=rse, vo=vo)
    locks = lock.get_dataset_locks_by_rse_id(rse_id=rse_id)

    for lock_object in locks:
        yield api_update_return_dict(lock_object)


def get_replica_locks_for_rule_id(rule_id, vo='def'):
    """
    Get the replica locks for a rule_id.

    :param rule_id:     Rule ID.
    :param vo:          The VO to act on.
    :return:            List of dicts.
    """

    locks = lock.get_replica_locks_for_rule_id(rule_id=rule_id)

    for lock_object in locks:
        if lock_object['scope'].vo != vo:  # rule is on a different VO, so don't return any locks
            LOGGER.debug('rule id %s is not present on VO %s' % (rule_id, vo))
            break
        yield api_update_return_dict(lock_object)
