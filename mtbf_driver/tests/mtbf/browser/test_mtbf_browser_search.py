# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import By, Wait, expected

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.search.app import Search


class TestBrowserSearch(GaiaMtbfTestCase):

    _google_search_input_locator = (By.NAME, 'q')

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.data_layer.enable_wifi()
        self.connect_to_local_area_network()

        self.search = Search(self.marionette)
        self.search.launch()

    def test_browser_search(self):
        search_text = 'Mozilla'
        self.browser = self.search.search_keyword(search_text)

        self.browser.switch_to_content()
        Wait(self.marionette, timeout=120).until(
                       expected.element_displayed(*self._google_search_input_locator))
        self.assertTrue(search_text in self.marionette.title)
        self.assertEqual(search_text,
                         self.marionette.find_element(*self._google_search_input_locator).get_attribute('value'))

    def tearDown(self):
        self.data_layer.disable_wifi()
        GaiaMtbfTestCase.tearDown(self)
