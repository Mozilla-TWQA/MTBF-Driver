# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.browser.app import Browser


class TestBrowserLAN(GaiaMtbfTestCase):

    _page_title_locator = (By.ID, 'page-title')

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.connect_to_local_area_network()

        self.browser = Browser(self.marionette)
        self.browser.launch()

    def test_browser_lan(self):
        """https://moztrap.mozilla.org/manage/case/1327/"""
        self.browser.go_to_url('http://mozqa.com/data/firefox/layout/mozilla.html')
        self.browser.switch_to_content()

        self.wait_for_element_present(*self._page_title_locator)
        heading = self.marionette.find_element(*self._page_title_locator)
        self.assertEqual(heading.text, 'We believe that the internet should be public, open and accessible.')

    def tearDown(self):
        GaiaMtbfTestCase.tearDown(self)
