# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from marionette import Wait

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from mtbf_driver.mtbf_apps.search.app import MTBF_Search


class TestBrowserNavigation(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.apps.set_permission_by_url(MTBF_Search.manifest_url, 'geolocation', 'deny')

        self.connect_to_network()
        self.test_url = 'http://mozqa.com/data/firefox/layout/mozilla.html'

        self.search = MTBF_Search(self.marionette)
        self.search.launch()

    def test_browser_back_button(self):
        browser = self.search.clean_and_go_to_url(self.test_url)

        browser.switch_to_content()
        Wait(self.marionette).until(lambda m: m.title == 'Mozilla')
        link = self.marionette.find_element(By.CSS_SELECTOR, '#community a')
        # TODO: remove the explicit scroll once bug 833370 is fixed
        self.marionette.execute_script(
            'arguments[0].scrollIntoView(false);', [link])
        link.tap()
        Wait(self.marionette).until(lambda m: m.title == 'Mozilla Community')

        browser.switch_to_chrome()
        browser.tap_back_button()
        browser.switch_to_content()
        Wait(self.marionette).until(lambda m: m.title == 'Mozilla')

        browser.switch_to_chrome()
        browser.tap_forward_button()
        browser.switch_to_content()
        Wait(self.marionette).until(lambda m: m.title == 'Mozilla Community')

    def tearDown(self):
        GaiaMtbfTestCase.tearDown(self)
