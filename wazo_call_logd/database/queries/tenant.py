# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .base import BaseDAO
from ..models import Tenant


class TenantDAO(BaseDAO):
    def create_all_uuids_if_not_exist(self, tenant_uuids):
        with self.new_session() as session:
            for tenant_uuid in tenant_uuids:
                if session.query(Tenant).get(tenant_uuid):
                    continue

                tenant = Tenant(uuid=tenant_uuid)
                session.add(tenant)
                session.flush()
