# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import expected, Wait
from gaiatest.apps.camera.app import Camera
from gaiatest.apps.base import Base


class Mtbf_Camera(Camera):

    def kill_abnormal_camera_app(self):
        Base.launch(self)
        viewfinder = Wait(self.marionette).until(expected.element_present(*self._viewfinder_video_locator))
        try:
            Wait(self.marionette, timeout=10).until(lambda m: m.execute_script('return arguments[0].readyState;', [viewfinder]) > 0)
        except:
            #Kill Camera app
            self.marionette.switch_to_frame()
            app_origin_name = self.marionette.execute_script("return GaiaApps.getRunningAppOrigin('%s');" % Camera.name)
            self.marionette.execute_async_script("GaiaApps.kill('%s');" % app_origin_name)
            result = self.marionette.execute_script('return GaiaApps.getDisplayedApp();')
            Wait(self.marionette).until(lambda m: result.get('name').lower() == 'default home screen')

