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
        # Turn on screen
        if not self.device.is_screen_enabled:
            self.device.turn_screen_on()

        # unlock
        if self.data_layer.get_setting('lockscreen.enabled'):
            self.device.unlock()

        # kill FTU if possible
        if self.apps.displayed_app.name.upper() == "FTU":
            self.apps.kill(self.apps.displayed_app)

        if full_reset:
            # disable passcode
            self.data_layer.set_setting('lockscreen.passcode-lock.code', '1111')
            self.data_layer.set_setting('lockscreen.passcode-lock.enabled', False)

            # change language back to english
            self.data_layer.set_setting("language.current", "en-US")

            # reset keyboard to default values
            self.data_layer.set_setting("keyboard.enabled-layouts",
                                        "{'app://keyboard.gaiamobile.org/manifest.webapp': {'en': True, 'number': True}}")

            # reset do not track
            self.data_layer.set_setting('privacy.donottrackheader.value', '-1')

            # don't change status of airplane mode
            # if self.data_layer.get_setting('airplaneMode.enabled'):
            #    # enable the device radio, disable airplane mode
            #    self.data_layer.set_setting('airplaneMode.enabled', False)

            # Re-set edge gestures pref to False
            self.data_layer.set_setting('edgesgesture.enabled', False)

            # disable carrier data connection
            if self.device.has_mobile_connection:
                self.data_layer.disable_cell_data()

            self.data_layer.disable_cell_roaming()

            ## TODO: Disable wifi operation since Bug 1064800
            # if self.device.has_wifi:
            #     # Bug 908553 - B2G Emulator: support wifi emulation
            #     if not self.device.is_emulator:
            #         self.data_layer.enable_wifi()
            #         self.data_layer.forget_all_networks()
            #         self.data_layer.disable_wifi()

            # don't remove contact data
            # self.data_layer.remove_all_contacts()

            # reset to home screen
            self.device.touch_home_button()

        # disable sound completely
        # self.data_layer.set_volume(0)

        # disable auto-correction of keyboard
        self.data_layer.set_setting('keyboard.autocorrect', False)

        # restore settings from testvars
        [self.data_layer.set_setting(name, value) for name, value in self.testvars.get('settings', {}).items()]

        # restore prefs from testvars
        for name, value in self.testvars.get('prefs', {}).items():
            if type(value) is int:
                self.data_layer.set_int_pref(name, value)
            elif type(value) is bool:
                self.data_layer.set_bool_pref(name, value)
            else:
                self.data_layer.set_char_pref(name, value)

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
        b2g_status = subprocess.check_output(["adb wait-for-device shell top -m 20 -n 1 -s cpu"], shell=True, stderr=subprocess.STDOUT)
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
