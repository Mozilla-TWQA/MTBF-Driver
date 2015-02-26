#!/usr/bin/python
from marionette import expected
from marionette import Wait
from marionette.by import By

from gaiatest.apps.music.app import Music

from mtbf_driver.mtbf_apps.music.regions.list_view import Mtbf_ListView

class Mtbf_Music(Music):
    _header_locator = (By.ID, "title")
    _top_bannder_locator = (By.CSS_SELECTOR, "#title-text")

    def back_from_playback(self):
        self.marionette.find_element(*self._header_locator).tap(25, 25)
        self.wait_for_element_displayed(*self._music_tiles_locator)

    def tap_songs_tab(self):
        element = Wait(self.marionette).until(
            expected.element_present(*self._songs_tab_locator))
        Wait(self.marionette).until(expected.element_displayed(element))
        element.tap()
        if self.marionette.find_element(*self._top_bannder_locator).text <> 'Songs':
            return Mtbf_ListView(self.marionette)
        else:
            return Mtbf_ListView(self.marionette,bolScrollingCheck=False)