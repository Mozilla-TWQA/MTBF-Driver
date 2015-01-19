# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from mtbf_driver.mtbf_apps.settings.app import MTBF_Settings


class TestSettingsBluetooth(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.settings = MTBF_Settings(self.marionette)
        self.settings.launch()

    def test_turn_on_and_off_bt(self):
        self.settings.go_back()

        self.bt_settings = self.settings.open_bluetooth_settings()
        self.wait_for_element_displayed(*self.bt_settings._bluetooth_label_locator)

        if not self.bt_settings.is_bluetooth_enabled:
            self.bt_settings.enable_bluetooth()
        if not self.bt_settings.is_visible_enabled:
            self.bt_settings.enable_visible_to_all()
        self.assertTrue(self.bt_settings.is_bluetooth_enabled, "Bluetooth not on via Settings app")
        self.assertTrue(self.bt_settings.is_visible_enabled, "Bluetooth not visible via Settings app")

        self.marionette.find_element(*self.bt_settings._bluetooth_label_locator).tap()
        self.wait_for_condition(lambda m: self.bt_settings.is_bluetooth_enabled == None)

    def tearDown(self):
        GaiaMtbfTestCase.tearDown(self)
