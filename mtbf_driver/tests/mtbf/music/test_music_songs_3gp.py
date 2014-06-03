# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from mtbf_driver.mtbf_apps.music.app import Mtbf_Music


class TestPlay3GPMusic(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)

        # add video to storage
        #self.push_resource('MUS_0001.3gp')

    def test_select_songs_play_3gp_file(self):
        """https://moztrap.mozilla.org/manage/case/4031/"""

        self.app_id = self.launch_by_touch("Music")
        self.apps.switch_to_displayed_app()
        music_app = Mtbf_Music(self.marionette)

        # switch to songs view
        list_view = music_app.tap_songs_tab()

        # check that songs (at least one) are available
        songs = list_view.media
        self.assertGreater(len(songs), 0, 'The 3gp file could not be found')

        player_view = songs[0].tap_first_song()

        self.wait_for_condition(
            lambda m: player_view.player_elapsed_time == '00:05',
            message='3gp sample did not start playing')

        # validate playback
        self.assertTrue(player_view.is_player_playing(), 'The player is not playing')

        # select stop
        player_view.tap_play()

        # validate stopped playback
        self.assertFalse(player_view.is_player_playing(), 'The player did not stop playing')
        music_app.back_from_playback()

    def tearDown(self):
        GaiaMtbfTestCase.tearDown(self)
