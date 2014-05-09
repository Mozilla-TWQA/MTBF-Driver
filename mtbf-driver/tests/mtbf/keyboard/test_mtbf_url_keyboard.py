# -*- coding: iso-8859-15 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from MtbfTestCase import GaiaMtbfTestCase
from gaiatest.mtbf_apps.ui_tests.app import UiTests
from gaiatest.mtbf_apps.ui_tests.app import MTBF_UiTests

class TestUrlKeyboard(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)

        self.app_id = self.launch_by_touch("UI tests")
        self.ui_tests = UiTests(self.marionette)
        self.mtbf_ui_tests = MTBF_UiTests(self.marionette)
        self.mtbf_ui_tests.back_to_main_screen()

    def test_url_keyboard(self):
        self.ui_tests.tap_ui_button()

        keyboard_page = self.ui_tests.tap_keyboard_option()
        keyboard_page.switch_to_frame()

        # tap the field "input type=url"
        keyboard = keyboard_page.tap_url_input()

        keyboard.switch_to_keyboard()
        # Test forward slash
        keyboard._tap('/')

        self.apps.switch_to_displayed_app()
        keyboard_page.switch_to_frame()
        typed_key = keyboard_page.url_input
        self.assertEqual(typed_key, u'/')

        # Test .com key
        keyboard.tap_dotcom()

        keyboard_page.switch_to_frame()
        typed_key = keyboard_page.url_input
        self.assertEqual(typed_key, u'/.com')

    def tearDown(self):
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.app_id)
        GaiaMtbfTestCase.tearDown(self)
