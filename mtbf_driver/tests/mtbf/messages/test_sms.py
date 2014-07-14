# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
import time
from gaiatest.apps.messages.app import Messages
from marionette.by import By


class TestSms(GaiaMtbfTestCase):


    def test_sms_send(self):
        """This test sends a text message to itself. It waits for a reply message.

        https://moztrap.mozilla.org/manage/case/1322/
        """
        self._text_message_content = "Automated Test %s" % str(time.time())
        self._last_message = ".message-list li"

        # launch the app
        self.launch_by_touch("sms")
        self.apps.switch_to_displayed_app()
        self.messages = Messages(self.marionette)
        self.messages.wait_for_message_list()

        # click new message
        new_message = self.messages.tap_create_new_message()
        new_message.type_phone_number(self.testvars['carrier']['phone_number'])

        new_message.type_message(self._text_message_content)

        #click send
        self.message_thread = new_message.tap_send()
        self.wait_for_condition(self.wait_for_last_message, 23)

    def tearDown(self):
        if hasattr(self, "message_thread"):
            self.apps.switch_to_displayed_app()
            self.message_thread.tap_back_button()
        GaiaMtbfTestCase.tearDown(self)

    def wait_for_last_message(self, m):
        self.apps.switch_to_displayed_app()
        messages = m.find_elements(By.CSS_SELECTOR, self._last_message)
        if len(messages) < 2:
            return False
        last_message = messages[-1]
        if "incoming" in last_message.get_attribute("class") and self._text_message_content in last_message.find_element(By.CSS_SELECTOR, ".bubble p").text :
            return True
        return False
