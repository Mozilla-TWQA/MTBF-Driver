# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.search.app import Search
from gaiatest.apps.homescreen.app import Homescreen


class TestBrowserBookmark(GaiaMtbfTestCase):

    _bookmark_added = False

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.connect_to_local_area_network()

        self.test_url = self.marionette.absolute_url('mozilla.html')

        curr_time = repr(time.time()).replace('.', '')
        self.bookmark_title = 'gaia%s' % curr_time[10:]

        self.homescreen = Homescreen(self.marionette)
        self.search = Search(self.marionette)
        self.search.launch()

    def test_browser_bookmark(self):
        self.browser = self.search.go_to_url(self.test_url)
        self.browser.tap_menu_button()
        bookmark = browser.tap_add_to_home()

        bookmark.type_bookmark_title(self.bookmark_title)
        bookmark.tap_add_bookmark_to_home_screen_dialog_button()

        # Switch to Home Screen to look for bookmark
        self.device.touch_home_button()

        self.homescreen = Homescreen(self.marionette)
        self.homescreen.wait_for_app_icon_present(self.bookmark_title)
        self._bookmark_added = homescreen.is_app_installed(self.bookmark_title)

        self.assertTrue(self._bookmark_added, 'The bookmark %s was not found to be installed on the home screen.' % self.bookmark_title)

    def tearDown(self):
        # make sure it goes back to the top for activating editing mode
        self.device.touch_home_button()
        self.device.touch_home_button()
        self.device.touch_home_button()
        self.device.touch_home_button()

        # Delete the bookmark
        self.homescreen.activate_edit_mode()
        self.homescreen.bookmark(self.bookmark_title).tap_delete_app().tap_confirm(bookmark=True)

        self.wait_for_condition(lambda m: self.apps.displayed_app.name == homescreen.name)
        self.apps.switch_to_displayed_app()
        self.homescreen.wait_for_bookmark_icon_not_present(self.bookmark_title)

        # Check that the bookmark icon is no longer displayed on the homescreen
        self._bookmark_added = homescreen.is_app_installed(self.bookmark_title)
        self.assertFalse(self._bookmark_added, 'The bookmark %s was not successfully removed from homescreen.' % self.bookmark_title)

        self.data_layer.disable_wifi()
        GaiaMtbfTestCase.tearDown(self)
