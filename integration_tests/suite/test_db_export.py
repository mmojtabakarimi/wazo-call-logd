# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import uuid

from datetime import (
    datetime as dt,
    timedelta as td,
    timezone as tz,
)
from hamcrest import (
    assert_that,
    calling,
    has_properties,
    not_none,
)
from wazo_test_helpers.hamcrest.raises import raises
from wazo_call_logd.database.models import Export
from wazo_call_logd.exceptions import ExportNotFoundException

from .helpers.base import DBIntegrationTest
from .helpers.database import export
from .helpers.constants import (
    MASTER_TENANT,
    OTHER_TENANT,
)


class TestDBExport(DBIntegrationTest):
    @export(path='exp1')
    @export(path='exp2', tenant_uuid=OTHER_TENANT)
    def test_get_tenant_filter(self, export1, export2):
        master_tenant = uuid.UUID(MASTER_TENANT)
        other_tenant = uuid.UUID(OTHER_TENANT)
        result = self.dao.export.get(export1['uuid'], [master_tenant])
        assert_that(result, has_properties(uuid=export1['uuid']))

        assert_that(
            calling(self.dao.export.get).with_args(export1['uuid'], [other_tenant]),
            raises(ExportNotFoundException),
        )

    @export()
    def test_export_filename(self, export):
        export = self.dao.export.get(export['uuid'])
        offset = export.requested_at.utcoffset() or td(seconds=0)
        date_utc = (export.requested_at - offset).replace(tzinfo=tz.utc)
        export_date_utc = date_utc.strftime('%Y-%m-%dT%H_%M_%SUTC')
        assert_that(
            export,
            has_properties(filename=f'{export_date_utc}-{export.uuid}.zip'),
        )

    def test_create(self):
        body = {
            'tenant_uuid': uuid.UUID(MASTER_TENANT),
            'user_uuid': uuid.uuid4(),
            'requested_at': dt.now(),
            'status': 'pending',
        }
        result = self.dao.export.create(Export(**body))
        assert_that(result, has_properties(uuid=not_none(), **body))

        self.session.query(Export).delete()
        self.session.commit()

    @export(status='processing', path=None)
    def test_update(self, export):
        export = self.dao.export.get(export['uuid'])
        export.status = 'error'
        export.path = '/tmp/test.zip'
        self.dao.export.update(export)

        result = self.dao.export.get(export.uuid)
        assert_that(result, has_properties(status='error', path='/tmp/test.zip'))
