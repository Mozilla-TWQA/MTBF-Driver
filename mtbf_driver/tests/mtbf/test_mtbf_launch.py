# -*- coding: iso-8859-15 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.music.app import Music


class TestMtbfLaunch(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)

    def test_launch(self):
        self.app_id = self.launch_by_touch("Music")
        #music_app = Music(self.marionette)
        #music_app.tap_albums_tab()

    def tearDown(self):
        GaiaMtbfTestCase.tearDown(self)
