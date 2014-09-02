# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from marionette.by import By
from marionette.marionette import Actions

from gaiatest.apps.base import PageRegion
from gaiatest.apps.homescreen.app import Homescreen


class MtbfHomescreen(Homescreen):

    def activate_edit_mode(self):
        self.apps.switch_to_displayed_app()
        time.sleep(1)
        app = self.marionette.find_element(*self._homescreen_all_icons_locator)
        Actions(self.marionette).\
            press(app).\
            wait(3).\
            release().\
            wait(1).\
            perform()
        self.wait_for_condition(lambda m: app.is_displayed())
        # Ensure that edit mode is active
        self.wait_for_condition(lambda m: self.is_edit_mode_active)

    def tap_collection(self, collection_name):
        for root_el in self.marionette.find_elements(*self._homescreen_all_icons_locator):
            if root_el.text == collection_name:
                self.marionette.execute_script(
                    'arguments[0].scrollIntoView(false);', [root_el])
                # TODO bug 1043293 introduced a timing/tap race issue here
                time.sleep(0.5)
                root_el.tap()
                from gaiatest.apps.homescreen.regions.collections import Collection
                return Collection(self.marionette)

    class InstalledApp(PageRegion):

        _delete_app_locator = (By.CSS_SELECTOR, 'span.remove')

        @property
        def name(self):
            return self.root_element.text

        def tap_icon(self):
            expected_name = self.name

            #TODO remove scroll after Bug 937053 is resolved
            self.marionette.execute_script(
                'arguments[0].scrollIntoView(false);', [self.root_element])

            # TODO bug 1043293 introduced a timing/tap race issue here
            time.sleep(0.5)
            self.root_element.tap(y=1)
            self.wait_for_condition(lambda m: self.apps.displayed_app.name.lower() == expected_name.lower())
            self.apps.switch_to_displayed_app()

        def tap_delete_app(self):
            """Tap on (x) to delete app"""
            self.root_element.find_element(*self._delete_app_locator).tap()

            from gaiatest.apps.homescreen.regions.confirm_dialog import ConfirmDialog
            return ConfirmDialog(self.marionette)
