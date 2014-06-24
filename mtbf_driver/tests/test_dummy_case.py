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
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_wait_for_5_minutes(self):
        time.sleep(300)
        self.assertEqual(1,1)

    def test_cpu_load(self):
        b2g_status = subprocess.check_output(["adb shell top -m 20 -n 1 -s cpu | grep b2g"])
        try:
            for li in b2g_status:
                percent = re.search("\\([0-9.]+s%)\\s", b2g_status).group[0]
        except Exception as e:
            logger.error(e)

    def test_page_source(self):
        try:
            with codecs.open("screenshot", "r+", encoding="utf-8") as f:
                last = f.read()
        except IOError:
            pass
        with codec.open("screenshot", "w+", encoding="utf-8") as f:
            self.apps.switch_to_displayed_app()
            current = self.marionette.page_source()
            f.seek(0)
            f.write(current)
            f.truncate()

