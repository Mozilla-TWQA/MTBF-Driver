# -*- coding: iso-8859-15 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.contacts.app import Contacts
from gaiatest.mocks.mock_contact import MockContact


class TestKeyboard(GaiaMtbfTestCase):

    _string = "aG1D2s3~!=@.#$^aśZïd".decode("UTF-8")

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        # Use the contacts app to enter some text
        self.contact = MockContact()
        self.contacts_app = Contacts(self.marionette)
        self.contacts_app.launch()

    def test_keyboard_basic(self):
        new_contact_form = self.contacts_app.tap_new_contact()
        new_contact_form.type_phone(self.contact['tel']['value'])
        new_contact_form.type_comment('')

        # initialize the keyboard app
        keyboard = new_contact_form.keyboard

        # send first 15 characters, delete last character, send a space, and send all others
        keyboard.send(self._string[:15])
        keyboard.tap_backspace()
        keyboard.tap_space()
        keyboard.send(self._string[15:])

        # select special character using extended character selector
        keyboard.choose_extended_character('A', 8)

        # go back to app frame and finish this
        self.apps.switch_to_displayed_app()
        new_contact_form.tap_done()
        self.wait_for_condition(lambda m: len(self.contacts_app.contacts) >= 1)

        contact_details = self.contacts_app.contacts[0].tap()
        output_text = contact_details.comments

        self.assertEqual(self._string[:14] + ' ' + self._string[15:] + 'Æ'.decode("UTF-8"), output_text)

    def tearDown(self):
        GaiaMtbfTestCase.tearDown(self)
        
