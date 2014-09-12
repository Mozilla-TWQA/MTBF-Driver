#!/usr/bin/python

from marionette.by import By
from gaiatest.apps.music.app import Music

class Mtbf_Music(Music):
    _header_locator = (By.ID, "title")

    def back_from_playback(self):
        self.marionette.find_element(*self._header_locator).tap(25, 25)
        self.wait_for_element_displayed(*self._music_tiles_locator)
