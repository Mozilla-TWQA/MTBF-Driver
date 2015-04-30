# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import codecs
import subprocess
import re
import logging


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

    def test_status_check(self):
        self.apps.switch_to_displayed_app()
        self._check_page_source()
        # sleep for 30s
        time.sleep(30)
        self.marionette.switch_to_frame()
        self.device.turn_screen_on()
        self.device.unlock()
        self.apps.switch_to_displayed_app()
        self._check_cpu_load()

    def _check_cpu_load(self):
        status = True
        b2g_status = subprocess.check_output(["adb shell top -m 20 -n 1 -s cpu"], shell=True, stderr=subprocess.STDOUT)
        try:
            for li in b2g_status:
                per = re.search('([0-9.]+s%)\s', b2g_status)
                if per:
                    percent = per.group[0]
                    logger.info("Cpu usage: " + percent + "%")
        except OSError as e:
            logger.error(e)
        self.assertEqual(status, True)

    def _check_page_source(self):
        status = True
        try:
            with codecs.open("screenshot", "r+", encoding="utf-8") as f:
                last = f.read()
                # TODO: compare last and current page source and see if screen is stuck
        except IOError:
            pass
        with codecs.open("screenshot", "w+", encoding="utf-8") as f:
            self.apps.switch_to_displayed_app()
            current = self.marionette.page_source
            f.seek(0)
            f.write(current)
            f.truncate()
        self.assertEqual(status, True)
