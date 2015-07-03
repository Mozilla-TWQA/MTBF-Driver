# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver.by import By
from gaiatest.apps.settings.app import Settings
import time

class MTBF_Settings(Settings):
    _header_text_locator = (By.CSS_SELECTOR, '#root > header > h1')
    _header_locator = (By.CSS_SELECTOR, '.current gaia-header')
    _icon_back_sign_locator = (By.CSS_SELECTOR, 'span.icon-back')
    _icon_cancel_locator = (By.CSS_SELECTOR, 'span.icon-close')
    _icon_back_locator = (By.ID, 'test-panel-back')
    _cellanddata_menu_locator = (By.ID, 'data-connectivity')

    def __init__(self, marionette):
        Settings.__init__(self, marionette)

    def wait_for_cellanddata(self):
        self.wait_for_condition(lambda m: m.find_element(*self._cellanddata_menu_locator).get_attribute('aria-disabled') != 'true')

    def go_back(self):
        self.wait_for_element_displayed(*self._header_locator)
        header = self.marionette.find_element(*self._header_locator)
        # TODO: replace this hard coded value with tap on the back button, after Bug 1061698 is fixed
        while not self.marionette.execute_script("return window.wrappedJSObject.Settings && window.wrappedJSObject.Settings._currentPanel === '#root'"):
            header.tap(x=10)
            time.sleep(5)

    def back_to_main_screen(self):
        while True:
            # if Settings header is in view, stop trying to go back
            header_text = self.marionette.find_element(*self._header_text_locator)
            if header_text.location.get('x') >= 0:
                break;

            # get all kinds of back buttons and go back
            icon_back_sign = self.marionette.find_elements(*self._icon_back_sign_locator)
            icon_cancel = self.marionette.find_elements(*self._icon_cancel_locator)
            icon_back = self.marionette.find_elements(*self._icon_back_locator)
            recover_icons = icon_back_sign + icon_cancel + icon_back
            for icon in recover_icons:
                if icon.is_displayed():
                    icon.tap()
                    # change to wait for title changes
                    time.sleep(3)
