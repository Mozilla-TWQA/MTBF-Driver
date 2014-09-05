# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.browser.app import Browser
from gaiatest.apps.browser.regions.html5_player import HTML5Player


class TestYouTube(GaiaMtbfTestCase):

    video_URL = 'http://m.youtube.com/watch?v=5MzuGWFIfio'
    acceptable_delay = 2.0

    # YouTube video locators
    _video_container_locator = (By.CSS_SELECTOR, 'div[style^="background-image"]')
    _video_element_locator = (By.TAG_NAME, 'video')

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.connect_to_network()

        self.browser = Browser(self.marionette)
        self.browser.launch()

    def test_play_youtube_video(self):
        """Confirm YouTube video playback
        https://moztrap.mozilla.org/manage/case/6073/
        """
        self.wait_for_element_displayed(*self.browser._awesome_bar_locator)
        self.marionette.find_element(*self.browser._awesome_bar_locator).clear()

        self.browser.go_to_url(self.video_URL, timeout=180)
        self.browser.switch_to_content()

        # Tap the video container to load the <video> element and start playing
        self.wait_for_element_displayed(*self._video_container_locator)
        self.marionette.find_element(*self._video_container_locator).tap()

        # Wait HTML5 player to appear
        self.wait_for_element_displayed(*self._video_element_locator)
        video = self.marionette.find_element(*self._video_element_locator)
        player = HTML5Player(self.marionette, video)

        # Check that video is playing
        player.wait_for_video_loaded()
        self.assertTrue(player.is_video_playing())

        # Pause playback
        player.pause()
        stopped_at = player.current_timestamp
        self.assertFalse(player.is_video_playing())

        # Resume playback
        player.play()
        resumed_at = player.current_timestamp
        self.assertTrue(player.is_video_playing())

    def tearDown(self):
        self.data_layer.disable_wifi()
        GaiaMtbfTestCase.tearDown(self)
