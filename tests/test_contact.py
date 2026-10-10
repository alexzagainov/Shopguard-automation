import allure
import pytest

from models.contact_form import ContactForm
from tests.base_test import BaseTest

# Chromium's text; Firefox/WebKit word it differently
REQUIRED_MESSAGE = "Please fill out this field."
SUCCESS_MESSAGE = "Success! Your details have been submitted successfully."


@allure.feature("Contact Us")
class TestContact(BaseTest):

    def send_contact_form(self, contact_form: ContactForm):
        self.header.contact_us()
        self.contact_us_page.fill_contact_form(contact_form)
        self.contact_us_page.upload_file()
        self.contact_us_page.submit()

    @allure.title("TC6: Contact Us form with all fields")
    def test_contact_form(self):
        self.send_contact_form(ContactForm())
        assert self.contact_us_page.get_success_message() == SUCCESS_MESSAGE

    @allure.title("Contact Us form without {field}")
    @pytest.mark.parametrize("field", [
        "email",
        # known bug: the site sends the form without these fields.
        # strict=True - if the site fixes it, the test fails with XPASS so the mark can be removed
        *[pytest.param(field, marks=pytest.mark.xfail(
            reason=f"BUG: the site doesn't require '{field}' in Contact Us", strict=True))
          for field in ["name", "subject", "message"]],
    ])
    def test_contact_form_unfilled_field(self, field):
        self.send_contact_form(ContactForm(**{field: ""}))
        # if the site accepted the form, the page changed and the field is gone
        assert self.contact_us_page.is_field_exist(field), \
            f"form was sent without '{field}' - the site doesn't require it"
        assert self.contact_us_page.get_field_validation_message(field) == REQUIRED_MESSAGE
