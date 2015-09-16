# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver.wait import Wait

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.search.app import Search
from gaiatest.apps.settings.app import Settings


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
        Wait(self.marionette, timeout=30).until(lambda m: m.title == 'Mozilla')

        self.apps.kill(search.app)
        self.device.touch_home_button()

        search.launch()
        Wait(self.marionette).until(lambda m: len(m.find_elements(*search._history_item_locator)) > 0)
        self.assertGreater(search.history_items_count, 0)

        self.settings = Settings(self.marionette)
        self.settings.launch()
        browsing_privacy = self.settings.open_browsing_privacy()

        browsing_privacy.tap_clear_browsing_history()
        browsing_privacy.tap_clear()

        self.device.touch_home_button()
        search.launch()
        search.wait_for_history_to_load(number_of_items=0)
        self.assertEqual(0, search.history_items_count)

    def tearDown(self):
        self.apps.kill(self.settings.app)
        self.data_layer.disable_cell_data()
        GaiaMtbfTestCase.tearDown(self)
