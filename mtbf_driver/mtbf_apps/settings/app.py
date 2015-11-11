# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import expected, By, Wait
from gaiatest.apps.settings.app import Settings
import time

class MTBF_Settings(Settings):
    _header_text_locator = (By.CSS_SELECTOR, '#root > header > h1')
    _header_locator = (By.CSS_SELECTOR, '.current gaia-header')
    _cellanddata_menu_locator = (By.ID, 'data-connectivity')
    _bluetooth_header_locator = (By.CSS_SELECTOR, '#bluetooth_v2 gaia-header')

    def __init__(self, marionette):
        Settings.__init__(self, marionette)

    @property
    def manifest_url(self):
        return '{}{}{}/manifest.webapp'.format(self.DEFAULT_PROTOCOL, 'settings', self.DEFAULT_APP_HOSTNAME)

    def wait_for_cellanddata(self):
        self.wait_for_condition(lambda m: m.find_element(*self._cellanddata_menu_locator).get_attribute('aria-disabled') != 'true')

    def enable_visible_to_all(self):
        _visible_to_all_label_locator = (By.CSS_SELECTOR, '#bluetooth_v2 .device-visible gaia-switch')
        # Bluetooth state is stored outside the profile bug 969310
        Wait(self.marionette, timeout=120).until(expected.element_displayed(*_visible_to_all_label_locator))
        self.marionette.find_element(*_visible_to_all_label_locator).tap()

    def tap_rename_my_device(self):
        _rename_my_device_button_locator = (By.CSS_SELECTOR, 'button.rename-device')
        _update_device_name_input_locator = (By.CSS_SELECTOR, 'input.settings-dialog-input')
        Wait(self.marionette, timeout=120).until(
            expected.element_displayed(*_rename_my_device_button_locator))
        rename_my_device_button = self.marionette.find_element(*_rename_my_device_button_locator)
        Wait(self.marionette).until(expected.element_enabled(rename_my_device_button))
        rename_my_device_button.tap()
        Wait(self.marionette, timeout=120).until(
            expected.element_displayed(*_update_device_name_input_locator))

    def enable_bluetooth(self):
        _bluetooth_label_locator = (By.CSS_SELECTOR, '#bluetooth_v2 .bluetooth-status gaia-switch')
        _bluetooth_checkbox_locator = (By.CSS_SELECTOR, '#bluetooth_v2 .bluetooth-rename button')
        self.marionette.find_element(*_bluetooth_label_locator).tap()
        Wait(self.marionette).until(expected.element_displayed(*_bluetooth_checkbox_locator))

    def disable_bluetooth(self):
        _bluetooth_label_locator = (By.CSS_SELECTOR, '#bluetooth_v2 .bluetooth-status gaia-switch')
        self.marionette.find_element(*_bluetooth_label_locator).tap()
