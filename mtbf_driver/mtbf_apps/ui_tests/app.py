# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.base import Base
from gaiatest.apps.ui_tests.app import UiTests
import time

class MTBF_UiTests(Base):
    _icon_back_sign_locator = (By.CSS_SELECTOR, 'span.icon-back')
    _icon_cancel_locator = (By.CSS_SELECTOR, 'span.icon-close')
    _icon_back_locator = (By.ID, 'test-panel-back')

    def __init__(self, marionette):
        Base.__init__(self, marionette)

    def back_to_main_screen(self):
        time.sleep(3)
        icon_back_sign = self.marionette.find_elements(*self._icon_back_sign_locator)
        icon_cancel = self.marionette.find_elements(*self._icon_cancel_locator)
        icon_back = self.marionette.find_elements(*self._icon_back_locator)
        recover_icons = icon_back_sign + icon_cancel + icon_back
        for icon in recover_icons:
            if icon.is_displayed():
                icon.tap()
                # change to wait for title changes
                time.sleep(3)
