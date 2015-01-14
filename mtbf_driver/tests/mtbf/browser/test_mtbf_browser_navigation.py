# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from marionette import Wait

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.search.app import Search


class TestBrowserNavigation(GaiaMtbfTestCase):

    _community_link_locator = (By.CSS_SELECTOR, '#community a')
    _community_history_section_locator = (By.ID, 'history')

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.connect_to_local_area_network()
        self.apps.set_permission_by_url(Search.manifest_url, 'geolocation', 'deny')

        self.test_url = self.marionette.absolute_url('mozilla.html')

        self.search = Search(self.marionette)
        self.search.launch()

    def test_browser_back_button(self):
        self.browser = search.go_to_url(self.test_url)
        self.browser.switch_to_content()

        Wait(self.marionette).until(lambda m: m.title == 'Mozilla')
        link = self.marionette.find_element(By.CSS_SELECTOR, '#community a')
        link.tap()
        Wait(self.marionette).until(lambda m: m.title == 'Mozilla Community')

        self.browser.switch_to_chrome()
        self.browser.tap_back_button()
        self.browser.switch_to_content()
        Wait(self.marionette).until(lambda m: m.title == 'Mozilla')

        self.browser.switch_to_chrome()
        self.browser.tap_forward_button()
        self.browser.switch_to_content()
        Wait(self.marionette).until(lambda m: m.title == 'Mozilla Community')

    def tearDown(self):
        GaiaMtbfTestCase.tearDown(self)
