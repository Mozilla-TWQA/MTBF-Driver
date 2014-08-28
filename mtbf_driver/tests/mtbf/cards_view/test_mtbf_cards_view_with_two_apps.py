# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import random
from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.system.regions.cards_view import CardsView
from marionette.marionette import Actions


class TestCardsView(GaiaMtbfTestCase):

    _test_apps = ['Messages', 'Clock']

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)

        # Launch the test apps
        for app in self._test_apps:
            self.apps.launch(app)

        # Switch to top level frame before starting the test
        self.marionette.switch_to_frame()

    def test_that_app_can_be_launched_from_cards_view(self):
        """https://moztrap.mozilla.org/manage/case/2462/"""

        cards_view = CardsView(self.marionette)
        self.assertFalse(cards_view.is_cards_view_displayed, 'Cards view not expected to be visible')

        # Pull up the cards view
        self.device.hold_home_button()
        cards_view.wait_for_cards_view()

        # Wait till it really displayed
        _cards_view_locator = ('id', 'cards-view')
        self.wait_for_condition(lambda m: m.find_element(*_cards_view_locator).is_displayed())

        time.sleep(5)
        cards = self.marionette.find_elements('css selector', 'ul#cards-list li.card')
        cards_num = len(cards)

        current = -1
        for i in range(cards_num):
            # parse the cards for the displayed card
            for attr in cards[i].get_attribute('style').split(';'):
                if 'opacity: 1' in attr:
                    current = i

        # if there is cards, don't run
        if current != -1:
            choose = random.randint(0, cards_num - 1)
            card_name = self.marionette.find_elements('css selector', 'ul#cards-list li.card')[choose].text

            current_frame = self.apps.displayed_app.frame
            final_x_position = current_frame.size['width']
            # start swipe from center of window
            start_x_position = final_x_position // 2
            start_y_position = current_frame.size['height'] // 2

            # swipe forward to get another app card
            move = choose - current
            if move > 0:
                final_x_position = final_x_position * (-1)
            if move != 0:
                for i in range(abs(move)):
                    Actions(self.marionette).flick(current_frame, start_x_position, start_y_position, final_x_position, start_y_position).perform()

            self.wait_for_condition(lambda m: 'opacity: 1;' in m.find_elements('css selector', 'ul#cards-list li.card')[choose].get_attribute('style'))
            self.marionette.find_elements('css selector', 'ul#cards-list li.card')[choose].tap()
            self.assertEqual(self.apps.displayed_app.name, card_name)

    def tearDown(self):
        self.device.touch_home_button()
        self.device.touch_home_button()
        GaiaMtbfTestCase.tearDown(self)
