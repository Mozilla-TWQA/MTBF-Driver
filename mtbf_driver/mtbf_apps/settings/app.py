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

    def open_bluetooth_settings(self):
        from mtbf_driver.mtbf_apps.settings.regions.bluetooth import MTBF_Bluetooth
        # this is technically visible, but needs scroll to be tapped
        # TODO Remove when bug 937053 is resolved
        bluetooth_menu_item = self.marionette.find_element(*self._bluetooth_menu_item_locator)
        self.marionette.execute_script("arguments[0].scrollIntoView(false);", [bluetooth_menu_item])
        self._tap_menu_item(self._bluetooth_menu_item_locator)
        return MTBF_Bluetooth(self.marionette)

    def back_to_main_screen(self):
        self.apps.switch_to_displayed_app()
        while True:
            # if Settings header is in view, stop trying to go back
            header = self.marionette.find_element(*self._header_locator)
            if header.text == "Settings":
                break;

            # temporary solution for tap "<" button
            header.tap(25, 25)
