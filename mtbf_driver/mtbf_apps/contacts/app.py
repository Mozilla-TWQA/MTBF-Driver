# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver.by import By
from marionette_driver import expected
from marionette_driver.errors import JavascriptException
from gaiatest.apps.contacts.app import Contacts
from marionette_driver.wait import Wait
from gaiatest.apps.base import Base


class MTBF_Contacts(Contacts):

    _edit_form_locator = (By.ID, 'view-contact-form')
    _edit_form_close_locator = (By.ID, 'contact-form-header')
    _cancel_search_button_locator = (By.ID, 'cancel-search')
    _search_field_area_locator = (By.CSS_SELECTOR, 'input[data-l10n-id="search-contact"]')
    _search_field_content_locator = (By.ID, 'search-contact')
    _search_result_contact_locator = (By.CSS_SELECTOR, '#search-list > li.contact-item > p.contact-text ')

    def launch(self):
        Base.launch(self)

        self.close_existing_edit_form()

        self.clear_search_view()

        Wait(self.marionette).until(expected.element_displayed(
            Wait(self.marionette).until(expected.element_present(
                *self._settings_button_locator))))

    def clear_search_view(self):
        if len(self.marionette.find_elements(*self._cancel_search_button_locator)) != 0:
            cancel_search_btn = self.marionette.find_element(*self._cancel_search_button_locator)
            if cancel_search_btn.is_displayed():
                cancel_search_btn.tap()

    def close_existing_edit_form(self):
        if len(self.marionette.find_elements(*self._edit_form_locator)) != 0:
            edit_form = self.marionette.find_element(*self._edit_form_locator)
            if "current" in edit_form.get_attribute('class'):
                self.apps.switch_to_displayed_app()
                self.marionette.execute_async_script("Accessibility.click(arguments[0].shadowRoot.querySelector('button.action-button'));",
                                                     [self.marionette.find_element(*self._edit_form_close_locator)],
                                                     special_powers=True)

    def search_contact(self, search_no):
        search_field_area = self.marionette.find_element(*self._search_field_area_locator)
        search_field_area.tap()
        search_field_content = self.marionette.find_element(*self._search_field_content_locator)
        search_field_content.send_keys(search_no)
        find_contact = self.marionette.find_element(*self._search_result_contact_locator)
        return self.Contact(self.marionette, find_contact)
