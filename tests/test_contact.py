import pytest
from playwright.sync_api import Page

from models.contact_form import ContactForm
from tests.base_test import BaseTest


class TestContact(BaseTest):

    __FILL_OUT_MESSAGE__ = "Please fill out this field."
    __SUCCESS_MESSAGE__ = "Success! Your details have been submitted successfully."

    @pytest.mark.parametrize("contact_form", [
        pytest.param(ContactForm(), id="fill all params"),
        pytest.param(ContactForm(name=""), id="name not filled"),
        pytest.param(ContactForm(email=""), id="email not filled"),
        pytest.param(ContactForm(subject=""), id="subject not filled"),
        pytest.param(ContactForm(message=""), id="message not filled"),
    ])
    def test_contact_page(self,contact_form: ContactForm):
        self.header.contact_us()
        self.contact_us_page.fill_contact_form(contact_form)
        self.contact_us_page.upload_file()
        self.contact_us_page.submit()
        if contact_form.name == "":

            assert self.contact_us_page.get_field_validation_message("name") == self.__FILL_OUT_MESSAGE__
        elif contact_form.email == "":
            assert self.contact_us_page.get_field_validation_message("email") == self.__FILL_OUT_MESSAGE__
        elif contact_form.subject == "":
            assert self.contact_us_page.get_field_validation_message("subject") == self.__FILL_OUT_MESSAGE__
        elif contact_form.message == "":
            assert self.contact_us_page.get_field_validation_message("message") == self.__FILL_OUT_MESSAGE__
        else:
            assert self.contact_us_page.get_success_message() == self.__SUCCESS_MESSAGE__







