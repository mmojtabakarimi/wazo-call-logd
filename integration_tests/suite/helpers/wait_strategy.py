# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import requests

from hamcrest import assert_that, has_entries, has_entry, only_contains
from wazo_test_helpers import until
from wazo_test_helpers.wait_strategy import WaitStrategy


class ComponentsWaitStrategy(WaitStrategy):
    def __init__(self, components):
        self._components = components

    def wait(self, integration_test):
        def components_are_ok(components):
            try:
                status = integration_test.call_logd.status.get()
            except requests.RequestException:
                status = {}

            assert_that(
                status,
                has_entries(
                    dict.fromkeys(self._components, value=has_entry('status', 'ok'))
                ),
            )

        until.assert_(components_are_ok, self._components, timeout=10)


class CallLogdEverythingUpWaitStrategy(WaitStrategy):
    def wait(self, integration_test):
        def everything_is_up():
            try:
                status = integration_test.call_logd.status.get()
            except requests.RequestException:
                status = {}

            component_statuses = [
                component['status']
                for component in status.values()
                if 'status' in component
            ]
            assert_that(component_statuses, only_contains('ok'))

        until.assert_(everything_is_up, timeout=10)
