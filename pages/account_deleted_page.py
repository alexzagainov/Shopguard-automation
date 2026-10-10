import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class AccountDeletedPage(BasePage):
    __ACCOUNT_DELETED_TITLE__ = '[data-qa="account-deleted"]'
    __CONTINUE_BUTTON__ = '[data-qa="continue-button"]'

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Get 'Account Deleted' title")
    def get_account_deleted_title(self) -> str:
        # text_content = the text in the HTML, not affected by CSS uppercase
        return self.page.locator(self.__ACCOUNT_DELETED_TITLE__).text_content().strip()

    @allure.step("Click 'Continue'")
    def continue_after_delete_account(self):
        self.click(self.__CONTINUE_BUTTON__)
