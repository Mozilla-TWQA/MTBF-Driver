# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.browser.app import Browser
from gaiatest.apps.homescreen.app import Homescreen


class TestBrowserBookmark(GaiaMtbfTestCase):

    _bookmark_added = False

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.connect_to_network()

        self.test_url = 'http://mozqa.com/data/firefox/layout/mozilla.html'

        curr_time = repr(time.time()).replace('.', '')
        self.bookmark_title = 'gaia%s' % curr_time[10:]

        self.homescreen = Homescreen(self.marionette)
        self.browser = Browser(self.marionette)
        self.browser.launch()

    def test_browser_bookmark(self):
        self.wait_for_element_displayed(*self.browser._awesome_bar_locator)
        self.marionette.find_element(*self.browser._awesome_bar_locator).clear()

        self.browser.go_to_url(self.test_url)
        self.browser.tap_bookmark_button()

        bookmark = self.browser.tap_add_bookmark_to_home_screen_choice_button()
        self.wait_for_element_displayed(*bookmark._bookmark_title_input_locator)
        bookmark.type_bookmark_title(self.bookmark_title)
        bookmark.tap_add_bookmark_to_home_screen_dialog_button()

        # Switch to Home Screen to look for bookmark
        self.device.touch_home_button()

        self.wait_for_element_displayed('id', 'bookmark-title')
        self.homescreen.wait_for_app_icon_present(self.bookmark_title)
        self._bookmark_added = self.homescreen.is_app_installed(self.bookmark_title)
        if self.find_element('id', 'edit-button').is_displayed():
            self.find_element('id', 'edit-button').tap()

        self.assertTrue(self._bookmark_added, 'The bookmark %s was not found to be installed on the home screen.' % self.bookmark_title)

    def tearDown(self):
        # make sure it goes back to the top for activating editing mode
        self.device.touch_home_button()
        self.device.touch_home_button()

        # delete the bookmark
        self.apps.switch_to_displayed_app()
        self.homescreen.activate_edit_mode()
        self.confirm_dialog = self.homescreen.installed_app(self.bookmark_title).tap_delete_app()
        self.confirm_dialog.tap_confirm()

        self.data_layer.disable_wifi()
        GaiaMtbfTestCase.tearDown(self)
