# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from mtbf_driver.mtbf_apps.settings.app import MTBF_Settings


class TestSettingsWifi(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.data_layer.enable_wifi()
        self.data_layer.forget_all_networks()
        self.data_layer.disable_wifi()
        self.settings = MTBF_Settings(self.marionette)
        self.settings.launch()

    def test_connect_to_wifi_via_settings_app(self):
        # we need to go back to main screen of settings app
        self.settings.go_back()

        wifi_settings = self.settings.open_wifi()
        # self.wait_for_element_displayed(*wifi_settings._wifi_enabled_label_locator)

        wifi_settings.enable_wifi()
        wifi_settings.connect_to_network(self.testvars['wifi'])

        # verify that wifi is now on
        self.assertTrue(self.data_layer.is_wifi_connected(self.testvars['wifi']), "WiFi was not connected via Settings app")

    def tearDown(self):
        self.data_layer.disable_wifi()
        GaiaMtbfTestCase.tearDown(self)
