# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from marionette.errors import TimeoutException
from gaiatest.apps.base import Base
from gaiatest.apps.homescreen.regions.bookmark_menu import BookmarkMenu


class MtbfBookmarkMenu(BookmarkMenu):

    name = "Bookmark"

    _edit_bookmark_to_home_screen_dialog_button_locator = (By.ID, 'edit-button')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_condition(lambda m: self.apps.displayed_app.name == self.name)
        self.apps.switch_to_displayed_app()

    def tap_add_bookmark_to_home_screen_dialog_button(self):
        self.wait_for_condition(lambda m: self.apps.displayed_app.name == self.name)
        # Check if it's a new bookmark or existing one
        try:
            self.apps.switch_to_displayed_app()
            self.wait_for_element_displayed(*self._add_bookmark_to_home_screen_dialog_button_locator)
            self.marionette.find_element(*self._add_bookmark_to_home_screen_dialog_button_locator).tap()
        except TimeoutException:
            self.apps.switch_to_displayed_app()
            self.wait_for_element_displayed(*self._edit_bookmark_to_home_screen_dialog_button_locator)
            self.marionette.find_element(*self._edit_bookmark_to_home_screen_dialog_button_locator).tap()

        # Wait for the Add to bookmark frame to be dismissed
        self.wait_for_condition(lambda m: self.apps.displayed_app.name != self.name)
        self.apps.switch_to_displayed_app()
