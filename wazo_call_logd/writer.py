# Copyright 2013-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class CallLogsWriter:
    def __init__(self, dao):
        self._dao = dao

    def write(self, call_logs):
        self._dao.call_log.delete_from_list(call_logs.call_logs_to_delete)
        self._dao.cel.unassociate_all_from_call_log_ids(call_logs.call_logs_to_delete)

        tenant_uuids = set(cdr.tenant_uuid for cdr in call_logs.new_call_logs)
        self._dao.tenant.create_all_uuids_if_not_exist(tenant_uuids)
        self._dao.call_log.create_from_list(call_logs.new_call_logs)
        self._dao.cel.associate_all_to_call_logs(call_logs.new_call_logs)
