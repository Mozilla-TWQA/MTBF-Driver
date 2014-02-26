# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os
import re
import sys
import time

from marionette import MarionetteTestCase
from marionette.by import By
from marionette.errors import NoSuchElementException
from marionette.errors import ElementNotVisibleException
from marionette.errors import TimeoutException
from marionette.errors import StaleElementException
from marionette.errors import InvalidResponseException

from gaiatest import *
from gaiatest import GaiaTestCase

class GaiaMtbfTestCase(GaiaTestCase):

    def __init__(self, *args, **kwargs):
        GaiaTestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        try:
            MarionetteTestCase.setUp(self)
        except InvalidResponseException:
            if self.restart:
                pass

        self.device = GaiaDevice(self.marionette, self.testvars)
        if self.device.is_android_build:
            self.device.add_device_manager(self.device_manager)
        if self.restart and (self.device.is_android_build or self.marionette.instance):
            self.device.stop_b2g()
            if self.device.is_android_build:
                self.cleanup_data()
            self.device.start_b2g()

       # we need to set the default timeouts because we may have a new session
        if self.marionette.timeout is not None:
            self.marionette.timeouts(self.marionette.TIMEOUT_SEARCH, self.marionette.timeout)
            self.marionette.timeouts(self.marionette.TIMEOUT_SCRIPT, self.marionette.timeout)
            self.marionette.timeouts(self.marionette.TIMEOUT_PAGE, self.marionette.timeout)
        else:
            self.marionette.timeouts(self.marionette.TIMEOUT_SEARCH, 10000)
            self.marionette.timeouts(self.marionette.TIMEOUT_PAGE, 30000)

        self.marionette.switch_to_frame()
        time.sleep(1)
        if len(self.marionette.find_elements("css selector", "iframe[data-frame-origin*=ftu]")) != 0:
            js = os.path.abspath(os.path.join(__file__, os.path.pardir, 'atoms', "gaia_apps.js"))
            self.marionette.import_script(js)
            result = self.marionette.execute_async_script("GaiaApps.kill('app://communications.gaiamobile.org/ftu/index.html');")

        self.lockscreen = LockScreen(self.marionette)
        self.apps = GaiaApps(self.marionette)
        self.data_layer = GaiaData(self.marionette, self.testvars)
        from gaiatest.apps.keyboard.app import Keyboard
        self.keyboard = Keyboard(self.marionette)

        # unlock screen and go back to home screen
        self.lockscreen.unlock()
        self.data_layer.set_setting("keyboard.ftu.enabled", False)
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")

        if self.restart:
            self.cleanup_gaia(full_reset=False)
        else:
            self.cleanup_gaia(full_reset=True)

        # always sleep 4 seconds before starting
        time.sleep(4)

    def launch_by_touch(self, name, switch_to_frame=True, url=None, launch_timeout=None):
        from gaiatest.apps.homescreen.app import Homescreen
        homescreen = Homescreen(self.marionette)
        self.marionette.switch_to_frame(self.apps.displayed_app.frame)
 
        icon = self.marionette.find_element('css selector', 'li[aria-label="' + name + '"]')
        while not icon.is_displayed() and homescreen.homescreen_has_more_pages:
            homescreen.go_to_next_page()

        while not icon.is_displayed() and self.marionette.execute_script("""var pageHelper = window.wrappedJSObject.GridManager.pageHelper;return pageHelper.getCurrentPageNumber() > 0;"""):
            self.marionette.execute_script('window.wrappedJSObject.GridManager.goToPreviousPage()')
        icon.tap()

        pt = re.compile("_|-")
        lowered_name = pt.sub("", name).split(' ')[0].lower()
        self.marionette.switch_to_frame()
        app = self.marionette.find_element('css selector', "iframe[mozapp^='app://" + lowered_name + "'][mozapp$='manifest.webapp']")

        iframe_id = app.get_attribute('id')
        if switch_to_frame:
            self.marionette.switch_to_frame(iframe_id)

        return iframe_id

    def cleanup_gaia(self, full_reset=True):
        # remove media
        if self.device.is_android_build:
            for filename in self.data_layer.media_files:
                self.device.manager.removeFile(filename)

        # switch off keyboard FTU screen
        self.data_layer.set_setting("keyboard.ftu.enabled", False)

        # restore settings from testvars
        [self.data_layer.set_setting(name, value) for name, value in self.testvars.get('settings', {}).items()]

        # unlock
        self.lockscreen.unlock()

        if full_reset:
            # disable passcode
            self.data_layer.set_setting('lockscreen.passcode-lock.code', '1111')
            self.data_layer.set_setting('lockscreen.passcode-lock.enabled', False)

            # change language back to english
            self.data_layer.set_setting("language.current", "en-US")

            # switch off spanish keyboard
            self.data_layer.set_setting("keyboard.layouts.spanish", False)

            # reset do not track
            self.data_layer.set_setting('privacy.donottrackheader.value', '-1')

            if self.data_layer.get_setting('ril.radio.disabled'):
                # enable the device radio, disable airplane mode
                self.data_layer.set_setting('ril.radio.disabled', False)

            # disable carrier data connection
            if self.device.has_mobile_connection:
                self.data_layer.disable_cell_data()

            self.data_layer.disable_cell_roaming()

            if self.device.has_wifi:
                # Bug 908553 - B2G Emulator: support wifi emulation
                if not self.device.is_emulator:
                    self.data_layer.enable_wifi()
                    self.data_layer.forget_all_networks()
                    self.data_layer.disable_wifi()

            # remove data
            self.data_layer.remove_all_contacts()

            # reset to home screen
            self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")

        # disable sound completely
        self.data_layer.set_volume(0)

    def tearDown(self):
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")
        time.sleep(2)
        MarionetteTestCase.tearDown(self)

