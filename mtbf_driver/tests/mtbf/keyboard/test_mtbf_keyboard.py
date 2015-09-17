# -*- coding: iso-8859-15 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from mtbf_driver.mtbf_apps.contacts.app import MTBF_Contacts
from gaiatest.mocks.mock_contact import MockContact


class TestKeyboard(GaiaMtbfTestCase):

    _string = "aG1 2Ds3~!=@.#$^aśZîd".decode("UTF-8")

    def test_keyboard_basic(self):
        # Use the contacts app to enter some text
        self.contact = MockContact()
        self.contacts_app = MTBF_Contacts(self.marionette)

        self.contacts_app.launch()
        new_contact_form = self.contacts_app.tap_new_contact()
        new_contact_form.type_phone(self.contact['tel']['value'])
        new_contact_form.keyboard.dismiss()
        new_contact_form.tap_comment()

        # send first 15 characters, delete last character, send a space, and send all others
        new_contact_form.keyboard.send(self._string[:15])
        new_contact_form.keyboard.tap_backspace()
        new_contact_form.keyboard.tap_space()
        new_contact_form.keyboard.send(self._string[15:])

        # select special character using extended character selector
        # Now the menu would include the original char, so the index should +1
        new_contact_form.keyboard.choose_extended_character('A', 9)

        # go back to app frame and finish this
        self.apps.switch_to_displayed_app()
        new_contact_form.tap_done()
        self.wait_for_condition(lambda m: len(self.contacts_app.contacts) >= 1)

        contact_details = self.contacts_app.contacts[0].tap()
        output_text = contact_details.comments

        self.assertEqual(self._string[:14] + ' ' + self._string[15:] + 'Æ'.decode("UTF-8"), output_text)

        contact_details.tap_back()
