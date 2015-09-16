# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import By, Wait, expected
from gaiatest import GaiaData
from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.search.app import Search

class TestBrowserCellData(GaiaMtbfTestCase):

    _page_title_locator = (By.ID, 'page-title')

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.data_layer.disable_wifi()
        self.data_layer.disable_cell_data()

        self.data_layer = GaiaData(self.marionette)
        self.data_layer.connect_to_cell_data()

        self.search = Search(self.marionette)
        self.search.launch()

    def test_browser_cell_data(self):
        """https://moztrap.mozilla.org/manage/case/1328/"""

        self.browser = self.search.go_to_url('http://mozqa.com/data/firefox/layout/mozilla.html')
        self.browser.wait_for_page_to_load(120)

        self.browser.switch_to_content()

        heading = Wait(self.marionette, timeout=120).until(expected.element_present(*self._page_title_locator))
        self.assertEqual(heading.text, 'We believe that the internet should be public, open and accessible.')

    def tearDown(self):
        self.marionette.switch_to_frame()
        self.data_layer.disable_cell_data()
        GaiaMtbfTestCase.tearDown(self)
