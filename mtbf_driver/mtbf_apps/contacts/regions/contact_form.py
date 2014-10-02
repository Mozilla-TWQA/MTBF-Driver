#!/usr/bin/python

from gaiatest.apps.contacts.regions.contact_form import ContactForm
from gaiatest.apps.contacts.regions.contact_form import NewContact


class MtbfContactForm(ContactForm):
    def type_phone(self, value):
        element = self.marionette.find_element(*self._phone_locator)
        element.clear()
        element.send_keys(value)


class MtbfNewContact(MtbfContactForm, NewContact):
    def __init__(self, marionette):
        MtbfContactForm.__init__(self, marionette)
        done = self.marionette.find_element(*self._done_button_locator)
        self.wait_for_condition(lambda m: done.location['y'] == 0)
