# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.phone.app import Phone


class TestCallLogAllCalls(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)

        # delete any existing call log entries - call log needs to be loaded
        self.phone = Phone(self.marionette)
        self.phone.launch()

    def test_call_log_all_calls(self):
        """https://moztrap.mozilla.org/manage/case/1306/"""

        call_log = self.phone.tap_call_log_toolbar_button()
        self.wait_for_element_displayed("css selector", "div.view-body")
        current_calls_count = call_log.all_calls_count
        numbers = self.marionette.find_elements("css selector", "div.view-body article ol li:first-child")
        if len(numbers) > 0:
            verification_bit = 1
            if self.testvars['remote_phone_number'] in numbers[0].text:
                verification_bit = 0

        test_phone_number = self.testvars['remote_phone_number']

        self.phone.tap_keypad_toolbar_button()

        # Make a call so it will appear in the call log
        self.phone.make_call_and_hang_up(test_phone_number)

        # Wait for fall back to phone app
        self.wait_for_condition(lambda m: self.apps.displayed_app.name == self.phone.name)
        self.apps.switch_to_displayed_app()

        call_log = self.phone.tap_call_log_toolbar_button()
        call_log.tap_all_calls_tab()

        # Check that 'All calls' tab is selected
        self.assertTrue(call_log.is_all_calls_tab_selected)

        # Now check that one call appears in the call log
        self.wait_for_condition(lambda m: call_log.all_calls_count > 0)
        self.assertEqual(call_log.all_calls_count, current_calls_count+verification_bit)

        # Check that the call displayed is for the call we made
        self.assertIn(test_phone_number, call_log.first_all_call_text)

    def tearDown(self):

        # In case the assertion fails this will still kill the call
        # An open call creates problems for future tests
        self.data_layer.kill_active_call()

        GaiaMtbfTestCase.tearDown(self)
