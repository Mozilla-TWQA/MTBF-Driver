# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from MtbfTestCase import GaiaMtbfTestCase

class DummyTestCase(GaiaMtbfTestCase):
    def __init__(self, *args, **kwargs):
        GaiaMtbfTestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        pass

    def TearDown(self):
        pass

    def test_wait_for_10_mins(self):
        time.sleep(600)
