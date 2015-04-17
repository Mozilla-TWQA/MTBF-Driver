# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import codecs
import logging
import subprocess
import time
import os
import re


from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DummyTestCase(GaiaMtbfTestCase):
    # TODO: bug 1147731 will change the behavior of lock, unlock screen, very possible to damage this test
    def cleanup_gaia(self, full_reset=True):
        pass

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.marionette.switch_to_frame()
        self.device.turn_screen_off()

    def test_charge(self):
        if os.getenv("CHARGE_HOUR"):
            time.sleep( int(os.getenv("CHARGE_HOUR")) * 60 * 60 )
        else:
            time.sleep( 7200 )
        self.marionette.switch_to_frame()
        self.device.turn_screen_on()
        self.device.unlock()
