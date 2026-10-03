import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):

    __SIGN_UP_NAME__=  '[name="name"]'
    __SIGN_UP_EMAIL__ = '[data-qa="signup-email"]'
    __SIGN_IN_EMAIL__ = '[data-qa="login-email"]'
    __SIGN_IN_PASSWORD__ = '[data-qa="login-password"]'
    __LOGIN_BUTTON__ ='[data-qa="login-button"]'
    __SIGN_UP_BUTTON__ = '[data-qa="signup-button"]'
    __SIGN_IN_ERROR_MESSAGE__ = '.login-form p'
    __SIGN_UP_ERROR_MESSAGE__ = '.signup-form p'
    __SIGN_UP_REQUIRED_FIELDS__ = {
        "name": __SIGN_UP_NAME__,
        "email": __SIGN_UP_EMAIL__,
    }

    __SIGN_IN_REQUIRED_FIELDS__ = {
        "email": __SIGN_IN_EMAIL__,
        "password": __SIGN_IN_PASSWORD__
    }

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Login with email {email} and password {password}")
    def login(self, email: str, password: str):
        self.fill_text(self.__SIGN_IN_EMAIL__, email)
        self.fill_text(self.__SIGN_IN_PASSWORD__, password)
        self.click(self.__LOGIN_BUTTON__)

    @allure.step("Start sign up with name {name} and email {email}")
    def sign_up(self, name:str, email:str):
        self.fill_text(self.__SIGN_UP_NAME__, name)
        self.fill_text(self.__SIGN_UP_EMAIL__, email)
        self.click(self.__SIGN_UP_BUTTON__)

    @allure.step("Get sign up validation message of {field}")
    def get_sign_up_validation_message(self, field: str) -> str:
        return self.get_validation_message(self.__SIGN_UP_REQUIRED_FIELDS__[field])

    @allure.step("Get login validation message of {field}")
    def get_sign_in_validation_message(self, field: str) -> str:
        return self.get_validation_message(self.__SIGN_IN_REQUIRED_FIELDS__[field])

    @allure.step("Get login error message")
    def get_sign_in_error_message(self) -> str:
        return self.get_text(self.__SIGN_IN_ERROR_MESSAGE__)

    @allure.step("Get sign up error message")
    def get_sign_up_error_message(self) -> str:
        return self.get_text(self.__SIGN_UP_ERROR_MESSAGE__)