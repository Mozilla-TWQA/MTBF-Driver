# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.base import Base
from gaiatest.apps.search.app import Search
import time

class MTBF_Search(Search, Base):

    name = 'Browser'
    manifest_url = "app://search.gaiamobile.org/manifest.webapp"

    def clean_and_go_to_url(self, url):
        self.marionette.find_element(*self._url_bar_locator).tap()
        clear = self.marionette.find_element('id', 'rocketbar-clear')
        if clear.is_displayed():
            clear.tap()
        self.marionette.find_element(*self._url_bar_locator).tap()

        from gaiatest.apps.homescreen.regions.search_panel import SearchPanel
        search_panel = SearchPanel(self.marionette)
        return search_panel.go_to_url(url)
