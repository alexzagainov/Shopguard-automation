import allure
from playwright.sync_api import Page, FilePayload

from models.contact_form import ContactForm
from pages.base_page import BasePage


class ContactUsPage(BasePage):
    _NAME = '[data-qa="name"]'
    _EMAIL = '[data-qa="email"]'
    _SUBJECT = '[data-qa="subject"]'
    _MESSAGE = '[data-qa="message"]'
    _CHOOSE_FILE = '[name="upload_file"]'
    _SUBMIT_BUTTON = '[data-qa="submit-button"]'
    _SUCCESS_MESSAGE = '.status.alert-success'

    _REQUIRED_FIELDS = {
        "name":_NAME,
        "email":_EMAIL,
        "subject":_SUBJECT,
        "message":_MESSAGE
    }

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Fill contact form")
    def fill_contact_form(self,contact_form: ContactForm):
        self.fill_text(self._NAME, contact_form.name)
        self.fill_text(self._EMAIL, contact_form.email)
        self.fill_text(self._SUBJECT, contact_form.subject)
        self.fill_text(self._MESSAGE, contact_form.message)

    @allure.step("Upload file {file_name}")
    def upload_file(self, file_name: str = "test.txt", content: str = "file for upload test"):
        # the file exists only in memory - nothing is created on the computer
        file = FilePayload(name=file_name, mimeType="text/plain", buffer=content.encode())
        self.page.locator(self._CHOOSE_FILE).set_input_files(files=file)

    @allure.step("Submit contact form")
    def submit(self):
        # the site asks "Press OK to proceed!" - click OK automatically
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.click(self._SUBMIT_BUTTON)

    @allure.step("Get success message")
    def get_success_message(self) -> str:
        return self.get_text(self._SUCCESS_MESSAGE)

    @allure.step("Check if success message is visible")
    def is_success_message_visible(self) -> bool:
        return self.is_visible(self._SUCCESS_MESSAGE)

    @allure.step("Check if field {field} exists")
    def is_field_exist(self, field: str) -> bool:
        return self.is_element_exist(self._REQUIRED_FIELDS[field])

    @allure.step("Get validation message of {field}")
    def get_field_validation_message(self, field: str) -> str:
        return self.get_validation_message(self._REQUIRED_FIELDS[field])





