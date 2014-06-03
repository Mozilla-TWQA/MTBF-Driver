# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.music.app import Music
from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase 

class TestMusic(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)

    def test_select_album_play(self):
        """https://moztrap.mozilla.org/manage/case/4031/"""

        self.app_id = self.launch_by_touch("Music")
        self.apps.switch_to_displayed_app()
        music_app = Music(self.marionette)

        # switch to albums view
        list_view = music_app.tap_albums_tab()

        # check that albums (at least one) are available
        albums = list_view.media
        self.assertGreater(len(albums), 0, 'The mp3 file could not be found')

        # select an album
        sublist_view = albums[0].tap_first_album()

        # select play
        # This wait is timing out because of bug 862156
        player_view = sublist_view.tap_play()

        # play for a short duration
        self.wait_for_condition(
            lambda m: player_view.player_elapsed_time == '00:05',
            message='Mp3 sample did not start playing')

        # validate playback
        self.assertTrue(player_view.is_player_playing(), 'The player is not playing')

        # select stop
        player_view.tap_play()

        # validate stopped playback
        self.assertFalse(player_view.is_player_playing(), 'The player did not stop playing')

    def tearDown(self):
        GaiaMtbfTestCase.tearDown(self)
