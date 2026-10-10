import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):

    _SIGN_UP_NAME=  '[name="name"]'
    _SIGN_UP_EMAIL = '[data-qa="signup-email"]'
    _SIGN_IN_EMAIL = '[data-qa="login-email"]'
    _SIGN_IN_PASSWORD = '[data-qa="login-password"]'
    _LOGIN_BUTTON ='[data-qa="login-button"]'
    _SIGN_UP_BUTTON = '[data-qa="signup-button"]'
    _SIGN_IN_ERROR_MESSAGE = '.login-form p'
    _SIGN_UP_ERROR_MESSAGE = '.signup-form p'
    _SIGN_UP_REQUIRED_FIELDS = {
        "name": _SIGN_UP_NAME,
        "email": _SIGN_UP_EMAIL,
    }

    _SIGN_IN_REQUIRED_FIELDS = {
        "email": _SIGN_IN_EMAIL,
        "password": _SIGN_IN_PASSWORD
    }

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Login with email {email} and password {password}")
    def login(self, email: str, password: str):
        self.fill_text(self._SIGN_IN_EMAIL, email)
        self.fill_text(self._SIGN_IN_PASSWORD, password)
        self.click(self._LOGIN_BUTTON)

    @allure.step("Start sign up with name {name} and email {email}")
    def sign_up(self, name:str, email:str):
        self.fill_text(self._SIGN_UP_NAME, name)
        self.fill_text(self._SIGN_UP_EMAIL, email)
        self.click(self._SIGN_UP_BUTTON)

    @allure.step("Get sign up validation message of {field}")
    def get_sign_up_validation_message(self, field: str) -> str:
        return self.get_validation_message(self._SIGN_UP_REQUIRED_FIELDS[field])

    @allure.step("Get login validation message of {field}")
    def get_sign_in_validation_message(self, field: str) -> str:
        return self.get_validation_message(self._SIGN_IN_REQUIRED_FIELDS[field])

    @allure.step("Get login error message")
    def get_sign_in_error_message(self) -> str:
        return self.get_text(self._SIGN_IN_ERROR_MESSAGE)

    @allure.step("Get sign up error message")
    def get_sign_up_error_message(self) -> str:
        return self.get_text(self._SIGN_UP_ERROR_MESSAGE)