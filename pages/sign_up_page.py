import allure
from typing import Optional

from playwright.sync_api import Page

from models.user import User
from pages.base_page import BasePage


class SignUpPage(BasePage):

    __MR_RADIO_BUTTON__=  '#id_gender1'
    __MRS_RADIO_BUTTON__= '#id_gender2'
    __NAME__= '#name'
    __PASSWORD__= '#password'
    __DAY_OF_BIRTH__= '#days'
    __MONTH_OF_BIRTH__= '#months'
    __YEAR_OF_BIRTH__= '#years'
    __NEWSLETTER_CHECKBOX__= '#newsletter'
    __SPECIAL_OFFERS_CHECKBOX__= '#optin'
    __FIRST_NAME__= '#first_name'
    __LAST_NAME__= '#last_name'
    __COMPANY__= '#company'
    __ADDRESS__= '#address1'
    __ADDRESS2__= '#address2'
    __COUNTRY__= '#country'
    __STATE__= '#state'
    __CITY__= '#city'
    __ZIPCODE__= '#zipcode'
    __MOBILE_NUMBER__= '#mobile_number'
    __CREATE_ACCOUNT_BUTTON__= '[data-qa="create-account"]'
    __ACCOUNT_CREATED_TITLE__= '[data-qa="account-created"]'
    __CONTINUE_BUTTTON__='[data-qa="continue-button"]'
    # keys = User field names, values = locators of fields marked "required" in the HTML
    __REQUIRED_FIELDS__ = {
        "name": __NAME__,
        "password": __PASSWORD__,
        "first_name": __FIRST_NAME__,
        "last_name": __LAST_NAME__,
        "address": __ADDRESS__,
        "state": __STATE__,
        "city": __CITY__,
        "zipcode": __ZIPCODE__,
        "mobile_number": __MOBILE_NUMBER__,
    }


    def __init__(self,page: Page):
        super().__init__(page)

    def fill_if_set(self, locator: str, value: Optional[str]):
        if value is not None:
            self.fill_text(locator, value)

    @allure.step("Fill account information form")
    def fill_the_signup_form(self, user: User):
        if user.title == "Mrs":
            self.check(self.__MRS_RADIO_BUTTON__)
        else:
            self.check(self.__MR_RADIO_BUTTON__)
        # email is filled on the previous page and is disabled here
        self.fill_text(self.__NAME__, user.name)
        self.fill_text(self.__PASSWORD__, user.password)
        self.select_option(self.__DAY_OF_BIRTH__, user.day_of_birth)
        self.select_option(self.__MONTH_OF_BIRTH__, user.month_of_birth)
        self.select_option(self.__YEAR_OF_BIRTH__, user.year_of_birth)
        if user.newsletter:
            self.check(self.__NEWSLETTER_CHECKBOX__)
        if user.special_offers:
            self.check(self.__SPECIAL_OFFERS_CHECKBOX__)
        self.fill_if_set(self.__FIRST_NAME__, user.first_name)
        self.fill_if_set(self.__LAST_NAME__, user.last_name)
        self.fill_if_set(self.__COMPANY__, user.company)
        self.fill_if_set(self.__ADDRESS__, user.address)
        self.fill_if_set(self.__ADDRESS2__, user.address2)
        self.select_option(self.__COUNTRY__, user.country)
        self.fill_if_set(self.__STATE__, user.state)
        self.fill_if_set(self.__CITY__, user.city)
        self.fill_if_set(self.__ZIPCODE__, user.zipcode)
        self.fill_if_set(self.__MOBILE_NUMBER__, user.mobile_number)

    @allure.step("Click 'Create Account'")
    def create_account(self):
        self.click(self.__CREATE_ACCOUNT_BUTTON__)

    @allure.step("Get 'Account Created' title")
    def get_account_created_title(self) -> str:
        # text_content = the text in the HTML, not affected by CSS uppercase
        return self.page.locator(self.__ACCOUNT_CREATED_TITLE__).text_content().strip()

    @allure.step("Get validation message of {field}")
    def get_field_validation_message(self, field: str) -> str:
        return self.get_validation_message(self.__REQUIRED_FIELDS__[field])

    @allure.step("Click 'Continue'")
    def continue_after_create_account(self):
        self.click(self.__CONTINUE_BUTTTON__)


