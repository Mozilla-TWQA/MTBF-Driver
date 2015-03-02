# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import expected
from marionette.marionette import Actions
from marionette import Wait

from gaiatest.apps.base import Base
from gaiatest.apps.camera.app import Camera


class MTBF_Camera(Camera, Base):

    def tap_switch_source(self):

        switch = self.marionette.find_element(*self._switch_button_locator)
        Wait(self.marionette).until(expected.element_displayed(switch))

        current_camera_mode = self.camera_mode
        # TODO: Use marionette.tap(_switch_button_locator) to switch camera mode
        Actions(self.marionette).press(switch).wait(1).move_by_offset(0, 0).release().perform()

        controls = self.marionette.find_element(*self._controls_locator)
        Wait(self.marionette).until(lambda m: controls.get_attribute('data-enabled') == 'true')

        Wait(self.marionette).until(lambda m: not current_camera_mode == self.camera_mode)
        self.wait_for_capture_ready()
