#!/usr/bin/python

from marionette.by import By
from gaiatest.apps.music.app import Music

class Mtbf_Music(Music):
    _back_button_locator = (By.ID, "title-back")

    def back_from_playback(self):
        self.marionette.find_element(*self._back_button_locator).tap()
        self.wait_for_element_displayed(*self._music_tiles_locator)
