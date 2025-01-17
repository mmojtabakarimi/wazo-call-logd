# Copyright 2017-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re
from datetime import datetime

from wazo_call_logd.database.models import Export

from .celery_tasks import export_recording_task

RECORDING_FILENAME_RE = re.compile(r'^.+-(\d+)-([a-z0-9-]{36})(.*)?$')


class CDRService:
    def __init__(self, dao):
        self._dao = dao

    def list(self, search_params):
        searched = search_params.get('search')
        rec_search_params = {}
        if searched:
            matches = RECORDING_FILENAME_RE.search(searched)
            if matches:
                del search_params['search']
                search_params['id'] = matches.group(1)
                rec_search_params['uuid'] = matches.group(2)
        call_logs = self._dao.call_log.find_all_in_period(search_params)
        rec_search_params['call_log_ids'] = [call_log.id for call_log in call_logs]
        count = self._dao.call_log.count_in_period(search_params)
        return {
            'items': call_logs,
            'filtered': count['filtered'],
            'total': count['total'],
        }

    def get(self, cdr_id, tenant_uuids):
        return self._dao.call_log.get_by_id(cdr_id, tenant_uuids)


class RecordingService:
    def __init__(self, dao, config, notifier):
        self._dao = dao
        self._config = config
        self._notifier = notifier

    def find_by(self, **kwargs):
        return self._dao.recording.find_by(**kwargs)

    def delete_media(self, cdr_id, recording_uuid, recording_path):
        self._dao.recording.delete_media_by(call_log_id=cdr_id, uuid=recording_uuid)
        if recording_path:
            os.remove(recording_path)

    def start_recording_export(
        self,
        recordings,
        user_uuid,
        tenant_uuid,
        destination_email,
        connection_info,
    ):
        recording_files = [
            {
                'uuid': recording.uuid,
                'filename': recording.filename,
                'path': recording.path,
                'call_log_id': recording.call_log_id,
            }
            for recording in recordings
        ]

        destination = self._config['exports']['directory']
        export_data = Export(
            user_uuid=user_uuid,
            tenant_uuid=tenant_uuid,
            requested_at=datetime.now(),
            status='pending',
        )
        export = self._dao.export.create(export_data)
        self._notifier.created(export)
        export_recording_task.apply_async(
            args=(
                export.uuid,
                recording_files,
                destination,
                tenant_uuid,
                destination_email,
                connection_info,
            ),
            task_id=str(export.uuid),
        )
        return {'uuid': export.uuid}
