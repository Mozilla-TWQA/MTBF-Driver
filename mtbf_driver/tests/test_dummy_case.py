# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase

class DummyTestCase(GaiaMtbfTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_wait_for_10_mins(self):
        time.sleep(300)
        self.assertEqual(1,1)
