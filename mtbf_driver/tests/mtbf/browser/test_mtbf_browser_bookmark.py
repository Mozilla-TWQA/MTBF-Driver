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

        curr_time = repr(time.time()).replace('.', '')
        self.bookmark_title = 'gaia%s' % curr_time[10:]

        self.browser = Browser(self.marionette)
        self.browser.launch()
        self.homescreen = Homescreen(self.marionette)

    def test_browser_bookmark(self):
        self.browser.go_to_url('http://mozqa.com/data/firefox/layout/mozilla.html')
        self.browser.tap_bookmark_button()

        bookmark = self.browser.tap_add_bookmark_to_home_screen_choice_button()
        bookmark.type_bookmark_title(self.bookmark_title)
        bookmark.tap_add_bookmark_to_home_screen_dialog_button()

        # Switch to Home Screen to look for bookmark
        self.device.touch_home_button()
        self._bookmark_added = self.homescreen.is_app_installed(self.bookmark_title)

        self.assertTrue(self._bookmark_added, 'The bookmark %s was not found to be installed on the home screen.' % self.bookmark_title)

    def tearDown(self):
        # make sure it goes back to the top for activating editing mode
        self.device.touch_home_button()
        self.device.touch_home_button()

        # delete the bookmark
        self.apps.switch_to_displayed_app()
        self.homescreen.activate_edit_mode()
        # this is a temporary solution
        self.homescreen.installed_app(self.bookmark_title).tap_delete_app()
        self.homescreen.installed_app(self.bookmark_title).tap_delete_app()

        self.marionette.switch_to_frame()
        page = self.marionette.find_element('css selector', 'iframe[data-url="app://bookmark.gaiamobile.org/remove.html"]')
        self.marionette.switch_to_frame(page)
        self.wait_for_element_displayed('id', 'remove-action')
        remove = self.marionette.find_element('id', 'remove-action')
        remove.tap()

        self.marionette.switch_to_frame()
        self.homescreen_frame_locator = ('css selector', '#homescreen iframe')
        homescreen = self.marionette.find_element(*self.homescreen_frame_locator)
        self.marionette.switch_to_frame(homescreen)
        
        self.marionette.find_element("id", "exit-edit-mode").tap()

        self.data_layer.disable_wifi()
        GaiaMtbfTestCase.tearDown(self)
