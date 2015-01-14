# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest import GaiaData
from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.search.app import Browser


class TestBrowserCellData(GaiaMtbfTestCase):

    _page_title_locator = (By.ID, 'page-title')

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.data_layer = GaiaData(self.marionette)
        self.data_layer.connect_to_cell_data()

        self.search = Search(self.marionette)
        self.search.launch()

    def test_browser_cell_data(self):
        """https://moztrap.mozilla.org/manage/case/1328/"""
        self.wait_for_element_displayed(*self.browser._awesome_bar_locator)
        self.marionette.find_element(*self.browser._awesome_bar_locator).clear()

        browser = search.go_to_url('http://mozqa.com/data/firefox/layout/mozilla.html')
        browser.wait_for_page_to_load(120)

        browser.switch_to_content()

        self.wait_for_element_present(*self._page_title_locator, timeout=120)
        heading = self.marionette.find_element(*self._page_title_locator)
        self.assertEqual(heading.text, 'We believe that the internet should be public, open and accessible.')

    def tearDown(self):
        self.data_layer.disable_cell_data()
        GaiaMtbfTestCase.tearDown(self)
