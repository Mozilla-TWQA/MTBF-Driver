# -*- coding: iso-8859-15 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from mtbf_driver.mtbf_apps.ui_tests.app import MTBF_UiTests


class TestNumberKeyboard(GaiaMtbfTestCase):

    def test_number_keyboard(self):
        self.app_id = self.launch_by_touch("uitest")
        self.mtbf_ui_tests = MTBF_UiTests(self.marionette)

        self.mtbf_ui_tests.back_to_main_screen()
        self.mtbf_ui_tests.tap_ui_button()

        keyboard_page = self.mtbf_ui_tests.tap_keyboard_option()
        keyboard_page.switch_to_frame()

        keyboard = keyboard_page.tap_number_input()

        self.assertEqual(str(keyboard.current_keyboard), 'number')

        keyboard.switch_to_keyboard()
        keyboard._tap('1')
        self.apps.switch_to_displayed_app()

        keyboard_page.switch_to_frame()
        typed_number = keyboard_page.number_input
        self.assertEqual(typed_number, u'1')
