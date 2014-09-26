# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.camera.app import Camera


class TestCamera(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)

        # Turn off geolocation prompt
        self.apps.set_permission('Camera', 'geolocation', 'deny')

        self.camera = Camera(self.marionette)
        self.camera.launch()

    def test_capture_a_video(self):
        """https://moztrap.mozilla.org/manage/case/2477/"""
        self.previous_number_of_videos = len(self.data_layer.video_files)

        # Switch to video mode
        self.camera.wait_for_capture_ready()
        camera = self.marionette.find_element('css selector', 'div[data-icon="camera"]')
        if not camera.is_displayed():
            self.camera.tap_switch_source()

        # Record 10 seconds of video
        self.camera.record_video(10)

        # Check that video saved to SD card
        self.wait_for_condition(lambda m: len(self.data_layer.video_files) == self.previous_number_of_videos + 1, 15)
        self.assertEqual(len(self.data_layer.video_files), self.previous_number_of_videos + 1)

    def tearDown(self):
        GaiaMtbfTestCase.tearDown(self)
