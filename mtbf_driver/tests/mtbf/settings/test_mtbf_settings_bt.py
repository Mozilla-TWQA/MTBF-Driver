# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import expected, By, Wait
from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from mtbf_driver.mtbf_apps.settings.app import MTBF_Settings as Settings

import time
from gaiatest import GaiaTestCase


class TestSettingsBluetooth(GaiaTestCase):

    def test_turn_on_and_off_bt(self):
        device_name = str(time.time())

        settings = Settings(self.marionette)
        settings.launch()

        self.assertFalse(self.data_layer.bluetooth_is_enabled)
        bluetooth_settings = settings.open_bluetooth()

        settings.enable_bluetooth()

        settings.tap_rename_my_device()
        bluetooth_settings.type_phone_name(device_name)
        bluetooth_settings.tap_update_device_name_ok()

        self.assertEquals(bluetooth_settings.device_name, device_name)

        settings.enable_visible_to_all()
        self.assertTrue(self.data_layer.bluetooth_is_discoverable)
        self.assertEquals(self.data_layer.bluetooth_name, device_name)

    def tearDown(self):
        self.marionette.switch_to_frame()
        self.data_layer.bluetooth_disable()
        GaiaTestCase.tearDown(self)
