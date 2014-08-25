# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from mtbf_driver.mtbf_apps.fmradio.app import MTBF_FmRadio


class TestFMRadioTurnOnOff(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)

        self.fm_radio = MTBF_FmRadio(self.marionette)
        self.fm_radio.launch()

    def test_turn_radio_on_off(self):
        """ Turn off and then Turn on the radio

        https://moztrap.mozilla.org/manage/case/1930/
        https://moztrap.mozilla.org/manage/case/1931/

        """
        self.apps.switch_to_displayed_app()
        self.wait_for_element_displayed(*self.fm_radio._power_button_locator)
        if self.fm_radio.is_power_button_on:
            self.fm_radio.tap_power_button()

        time.sleep(20)

        # check the radio is off
        self.fm_radio.wait_for_radio_off()

        self.assertFalse(self.data_layer.is_fm_radio_enabled)

        # turn the radio on
        self.fm_radio.tap_power_button()
        self.wait_for_condition(lambda m: self.data_layer.is_fm_radio_enabled)

        # check the radio is on
        self.assertTrue(self.fm_radio.is_power_button_on)
        self.assertTrue(self.data_layer.is_fm_radio_enabled)

    def tearDown(self):
        if self.fm_radio.is_power_button_on:
            self.fm_radio.tap_power_button()

        GaiaMtbfTestCase.tearDown(self)
