# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver.wait import Wait

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.search.app import Search
from mtbf_driver.mtbf_apps.settings.app import MTBF_Settings


class TestBrowserClearHistory(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.data_layer.enable_wifi()
        self.connect_to_local_area_network()

        self.test_url = self.marionette.absolute_url('mozilla.html')

    def test_browser_clear_history(self):
        """
        https://moztrap.mozilla.org/manage/cases/?filter-id=3582
        """
        search = Search(self.marionette)
        search.launch()
        browser = search.go_to_url(self.test_url)
        browser.switch_to_content()
        Wait(self.marionette).until(lambda m: m.title == 'Mozilla')

        self.device.touch_home_button()

        search.launch()
        Wait(self.marionette).until(lambda m: search.history_items_count > 0)
        self.assertGreater(search.history_items_count, 0)

        settings = MTBF_Settings(self.marionette)
        settings.launch()
        settings.go_back()
        browsing_privacy = settings.open_browsing_privacy_settings()

        browsing_privacy.tap_clear_browsing_history()
        browsing_privacy.tap_clear()

        self.device.touch_home_button()
        search.launch()
        search.wait_for_history_to_load(number_of_items=0)
        self.assertEqual(0, search.history_items_count)

    def tearDown(self):
        self.data_layer.disable_cell_data()
        GaiaMtbfTestCase.tearDown(self)
