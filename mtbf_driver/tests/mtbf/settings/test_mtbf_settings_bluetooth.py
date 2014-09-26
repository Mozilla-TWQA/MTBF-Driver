# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from mtbf_driver.mtbf_apps.settings.app import MTBF_Settings


class TestBluetoothSettings(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)

        self.settings = MTBF_Settings(self.marionette)
        self.settings.launch()

    def test_toggle_bluetooth_settings(self):
        device_name = str(time.time())

        bluetooth_settings = self.settings.open_bluetooth_settings()
        bluetooth_settings.enable_bluetooth()

        bluetooth_settings.tap_rename_my_device()
        bluetooth_settings.type_phone_name(device_name)
        bluetooth_settings.tap_update_device_name_ok()

        bluetooth_settings.enable_visible_to_all()
        bluetooth_settings.disable_bluetooth()

    def tearDown(self):
        self.settings.back_to_main_screen()
        GaiaMtbfTestCase.tearDown(self)
