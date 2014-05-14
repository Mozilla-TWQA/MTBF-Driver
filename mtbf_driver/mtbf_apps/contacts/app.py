# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.base import Base
from gaiatest.apps.contacts.app import Contacts
import time

class MTBF_Contacts(Contacts):
    _view_screenshot_locator = (By.CSS_SELECTOR, '#view-screenshot')
    _icon_back_sign_locator = (By.CSS_SELECTOR, 'span.icon-back')
    _icon_cancel_locator = (By.CSS_SELECTOR, 'span.icon-close')
    _icon_back_locator = (By.ID, 'test-panel-back')

    def __init__(self, marionette):
        Contacts.__init__(self, marionette)

    def back_contacts_list(self):
        self.apps.switch_to_displayed_app()
        while True:
            if not self.marionette.find_element(*self._view_screenshot_locator).is_displayed():
                break;

            # get all kinds of back buttons and go back
            back_icons = [
                self.marionette.find_elements(*self._icon_back_sign_locator),
                self.marionette.find_elements(*self._icon_cancel_locator),
                self.marionette.find_elements(*self._icon_back_locator)]
            from itertools import chain
            back_icons = chain.from_iterable(back_icons)
            for icon in back_icons:
                if icon.is_displayed():
                    icon.tap()
                    # change to wait for title changes
                    time.sleep(3)
