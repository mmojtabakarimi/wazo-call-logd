# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_call_logd.rest_api import api

from . import (
    http,
    service,
)


# This plugin is used for the tenant uuid migration between wazo-auth and webhookd
class Plugin(object):

    def load(self, dependencies):
        config = dependencies['config']
        tenant_upgrade_service = service.CallLogdTenantUpgradeService(config)
        api.add_resource(
            http.CallLogdTenantUpgradeResource,
            '/tenant-migration',
            resource_class_args=[tenant_upgrade_service],
        )
