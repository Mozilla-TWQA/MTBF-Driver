# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver.by import By
from gaiatest.apps.ui_tests.app import UiTests
from marionette_driver.errors import TimeoutException

class MTBF_UiTests(UiTests):
    _test_panel_header_locator = (By.CSS_SELECTOR, '#test-panel-header')

    def back_to_main_screen(self):
        try:
            self.wait_for_element_displayed(*self._test_panel_header_locator)
            self.marionette.find_element(*self._test_panel_header_locator).tap(25, 25)
            self.wait_for_element_not_displayed(*self._test_panel_header_locator)
        except TimeoutException:
            pass
