# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.browser.app import Browser


class TestBrowserTabs(GaiaMtbfTestCase):

    _page_title_locator = (By.ID, 'page-title')

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.connect_to_network()

        self.browser = Browser(self.marionette)
        self.browser.launch()

    def test_browser_tabs(self):
        # Remember the tabs number
        self.ori_tab_num = self.browser.displayed_tabs_number

        # Open tab menu.
        self.browser.tap_tab_badge_button()

        # Add a new tab and load a website.
        self.browser.tap_add_new_tab_button()
        self.browser.go_to_url('http://mozqa.com/data/firefox/layout/mozilla.html')
        self.browser.switch_to_content()
        self.wait_for_element_present(*self._page_title_locator)
        heading = self.marionette.find_element(*self._page_title_locator)
        self.assertEqual(heading.text, 'We believe that the internet should be public, open and accessible.')

        # Assert that the new tab has opened.
        self.browser.switch_to_chrome()
        self.assertEqual(self.browser.displayed_tabs_number, self.ori_tab_num+1)
        # Assert that the displayed tabs number is equal with the actual number of opened tabs.
        self.assertEqual(self.browser.displayed_tabs_number, self.browser.tabs_count)

        # Switch back to the first tab.
        self.browser.tap_tab_badge_button()
        self.browser.tabs[0].tap_tab()
        self.assertTrue(self.browser.is_awesome_bar_visible)

    def tearDown(self):
        self.data_layer.disable_wifi()
        GaiaMtbfTestCase.tearDown(self)
