# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.settings.regions.bluetooth import Bluetooth


class MTBF_Bluetooth(Bluetooth):

    def enable_bluetooth(self):
        if self.is_bluetooth_enabled != 'true':
            self.marionette.find_element(*self._bluetooth_label_locator).tap()
            self.wait_for_condition(lambda m: self.is_bluetooth_enabled == 'true')
            self.wait_for_condition(lambda m: m.find_element(*self._rename_my_device_button_locator).is_enabled())

    def disable_bluetooth(self):
        if self.is_bluetooth_enabled == 'true':
            self.marionette.find_element(*self._bluetooth_label_locator).tap()
            self.wait_for_condition(lambda m: self.is_bluetooth_enabled != 'true')
            self.wait_for_condition(lambda m: not m.find_element(*self._rename_my_device_button_locator).is_enabled())
