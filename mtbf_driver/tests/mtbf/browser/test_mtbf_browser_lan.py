# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from marionette import Wait

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from mtbf_driver.mtbf_apps.search.app import MTBF_Search


class TestBrowserLAN(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.connect_to_local_area_network()
        self.test_url = 'http://mozqa.com/data/firefox/layout/mozilla.html'

        self.search = MTBF_Search(self.marionette)
        self.search.launch()

    def test_browser_lan(self):
        """https://moztrap.mozilla.org/manage/case/1327/"""
        time.sleep(3)
        browser = self.search.clean_and_go_to_url(self.test_url)
        browser.switch_to_content()
        Wait(self.marionette).until(lambda m: m.title == 'Mozilla')

    def tearDown(self):
        self.data_layer.disable_wifi()
        GaiaMtbfTestCase.tearDown(self)
