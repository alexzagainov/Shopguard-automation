import allure
from typing import Optional

from playwright.sync_api import Page

from models.user import User
from pages.base_page import BasePage


class SignUpPage(BasePage):

    _MR_RADIO_BUTTON=  '#id_gender1'
    _MRS_RADIO_BUTTON= '#id_gender2'
    _NAME= '#name'
    _PASSWORD= '#password'
    _DAY_OF_BIRTH= '#days'
    _MONTH_OF_BIRTH= '#months'
    _YEAR_OF_BIRTH= '#years'
    _NEWSLETTER_CHECKBOX= '#newsletter'
    _SPECIAL_OFFERS_CHECKBOX= '#optin'
    _FIRST_NAME= '#first_name'
    _LAST_NAME= '#last_name'
    _COMPANY= '#company'
    _ADDRESS= '#address1'
    _ADDRESS2= '#address2'
    _COUNTRY= '#country'
    _STATE= '#state'
    _CITY= '#city'
    _ZIPCODE= '#zipcode'
    _MOBILE_NUMBER= '#mobile_number'
    _CREATE_ACCOUNT_BUTTON= '[data-qa="create-account"]'
    _ACCOUNT_CREATED_TITLE= '[data-qa="account-created"]'
    _CONTINUE_BUTTON='[data-qa="continue-button"]'
    # keys = User field names, values = locators of fields marked "required" in the HTML
    _REQUIRED_FIELDS = {
        "name": _NAME,
        "password": _PASSWORD,
        "first_name": _FIRST_NAME,
        "last_name": _LAST_NAME,
        "address": _ADDRESS,
        "state": _STATE,
        "city": _CITY,
        "zipcode": _ZIPCODE,
        "mobile_number": _MOBILE_NUMBER,
    }


    def __init__(self,page: Page):
        super().__init__(page)

    def fill_if_set(self, locator: str, value: Optional[str]):
        if value is not None:
            self.fill_text(locator, value)

    @allure.step("Fill account information form")
    def fill_the_signup_form(self, user: User):
        if user.title == "Mrs":
            self.check(self._MRS_RADIO_BUTTON)
        else:
            self.check(self._MR_RADIO_BUTTON)
        # email is filled on the previous page and is disabled here
        self.fill_text(self._NAME, user.name)
        self.fill_text(self._PASSWORD, user.password)
        self.select_option(self._DAY_OF_BIRTH, user.day_of_birth)
        self.select_option(self._MONTH_OF_BIRTH, user.month_of_birth)
        self.select_option(self._YEAR_OF_BIRTH, user.year_of_birth)
        if user.newsletter:
            self.check(self._NEWSLETTER_CHECKBOX)
        if user.special_offers:
            self.check(self._SPECIAL_OFFERS_CHECKBOX)
        self.fill_if_set(self._FIRST_NAME, user.first_name)
        self.fill_if_set(self._LAST_NAME, user.last_name)
        self.fill_if_set(self._COMPANY, user.company)
        self.fill_if_set(self._ADDRESS, user.address)
        self.fill_if_set(self._ADDRESS2, user.address2)
        self.select_option(self._COUNTRY, user.country)
        self.fill_if_set(self._STATE, user.state)
        self.fill_if_set(self._CITY, user.city)
        self.fill_if_set(self._ZIPCODE, user.zipcode)
        self.fill_if_set(self._MOBILE_NUMBER, user.mobile_number)

    @allure.step("Click 'Create Account'")
    def create_account(self):
        self.click(self._CREATE_ACCOUNT_BUTTON)

    @allure.step("Get 'Account Created' title")
    def get_account_created_title(self) -> str:
        # text_content = the text in the HTML, not affected by CSS uppercase
        return self.page.locator(self._ACCOUNT_CREATED_TITLE).text_content().strip()

    @allure.step("Get validation message of {field}")
    def get_field_validation_message(self, field: str) -> str:
        return self.get_validation_message(self._REQUIRED_FIELDS[field])

    @allure.step("Click 'Continue'")
    def continue_after_create_account(self):
        self.click(self._CONTINUE_BUTTON)


