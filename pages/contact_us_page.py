import allure
import pytest
from playwright.sync_api import Page, FilePayload

from models.contact_form import ContactForm
from pages.base_page import BasePage


class ContactUsPage(BasePage):
    __NAME__ = '[data-qa="name"]'
    __EMAIL__ = '[data-qa="email"]'
    __SUBJECT__ = '[data-qa="subject"]'
    __MESSAGE__ = '[data-qa="message"]'
    __CHOOSE_FILE__ = '[name="upload_file"]'
    __SUBMIT_BUTTON__ = '[data-qa="submit-button"]'
    __SUCCESS_MESSAGE__ = '.status.alert-success'

    __REQUIRED_FIELDS__ = {
        "name":__NAME__,
        "email":__EMAIL__,
        "subject":__SUBJECT__,
        "message":__MESSAGE__
    }

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Fill contact form")
    def fill_contact_form(self,contact_form: ContactForm):
        self.fill_text(self.__NAME__, contact_form.name)
        self.fill_text(self.__EMAIL__, contact_form.email)
        self.fill_text(self.__SUBJECT__, contact_form.subject)
        self.fill_text(self.__MESSAGE__, contact_form.message)

    @allure.step("Upload file {file_name}")
    def upload_file(self, file_name: str = "test.txt", content: str = "file for upload test"):
        # the file exists only in memory - nothing is created on the computer
        file = FilePayload(name=file_name, mimeType="text/plain", buffer=content.encode())
        self.page.locator(self.__CHOOSE_FILE__).set_input_files(files=file)

    @allure.step("Submit contact form")
    def submit(self):
        # the site asks "Press OK to proceed!" - click OK automatically
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.click(self.__SUBMIT_BUTTON__)

    @allure.step("Get success message")
    def get_success_message(self) -> str:
        return self.get_text(self.__SUCCESS_MESSAGE__)

    @allure.step("Check if success message is visible")
    def is_success_message_visible(self) -> bool:
        return self.page.locator(self.__SUCCESS_MESSAGE__).is_visible()

    @allure.step("Check if field {field} exists")
    def is_field_exist(self, field: str) -> bool:
        return self.is_element_exist(self.__REQUIRED_FIELDS__[field])

    @allure.step("Get validation message of {field}")
    def get_field_validation_message(self, field: str) -> str:
        if self.is_element_exist(self.__REQUIRED_FIELDS__[field]):
            return self.get_validation_message(self.__REQUIRED_FIELDS__[field])
        else:
            pytest.fail(f"Field {field} does not exist")
            return ""





