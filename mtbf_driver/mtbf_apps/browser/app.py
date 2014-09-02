# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import time

from gaiatest.apps.base import PageRegion
from gaiatest.apps.browser.app import Browser
from mtbf_apps.homescreen.regions.bookmark_menu import MtbfBookmarkMenu as BookmarkMenu


class MtbfBrowser(Browser):

    def tap_add_bookmark_to_home_screen_choice_button(self):
        self.wait_for_element_displayed(*self._add_bookmark_to_home_screen_choice_locator)
        self.marionette.find_element(*self._add_bookmark_to_home_screen_choice_locator).tap()
        return BookmarkMenu(self.marionette)

