import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class AccountDeletedPage(BasePage):
    _ACCOUNT_DELETED_TITLE = '[data-qa="account-deleted"]'
    _CONTINUE_BUTTON = '[data-qa="continue-button"]'

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Get 'Account Deleted' title")
    def get_account_deleted_title(self) -> str:
        # text_content = the text in the HTML, not affected by CSS uppercase
        return self.page.locator(self._ACCOUNT_DELETED_TITLE).text_content().strip()

    @allure.step("Click 'Continue'")
    def continue_after_delete_account(self):
        self.click(self._CONTINUE_BUTTON)
