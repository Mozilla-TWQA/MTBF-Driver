# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from marionette import Wait


from gaiatest.apps.base import Base
from gaiatest.apps.music.regions.list_view import ListView


class Mtbf_ListView(ListView):

    def __init__(self, marionette, bolScrollingCheck=True):
        Base.__init__(self, marionette)
        if bolScrollingCheck:
            Wait(self.marionette).until(
                lambda m: self.marionette.find_element(*self._view_locator).get_attribute('class') == 'scrolling')
        Wait(self.marionette).until(
            lambda m: self.marionette.find_element(*self._view_locator).get_attribute('class') != 'scrolling')
