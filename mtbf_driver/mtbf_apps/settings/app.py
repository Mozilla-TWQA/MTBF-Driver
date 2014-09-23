# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.settings.app import Settings
import time

class MTBF_Settings(Settings):
    _header_locator = (By.CSS_SELECTOR, '.current gaia-header')
    _cellanddata_menu_locator = (By.ID, 'data-connectivity')

    def __init__(self, marionette):
        Settings.__init__(self, marionette)

    def wait_for_cellanddata(self):
        self.wait_for_condition(lambda m: m.find_element(*self._cellanddata_menu_locator).get_attribute('aria-disabled') != 'true')

    def back_to_main_screen(self):
        self.apps.switch_to_displayed_app()
        while True:
            # if Settings header is in view, stop trying to go back
            header = self.marionette.find_element(*self._header_locator)
            if header.text == "Settings":
                break;

            # temporary solution for tap "<" button
            header.tap(25, 25)
