import allure
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage


class Footer(BasePage):
    __SUBSCRIPTION_EMAIL__ = "#susbscribe_email"   # the site really spells it "susbscribe"
    __SUBSCRIPTION_BUTTON__ = "#subscribe"
    # always in the HTML but hidden - it's shown for ~1.5 seconds after subscribing
    __SUBSCRIBE_SUCCESS__ = "#success-subscribe"

    @allure.step("Fill subscription email: {email}")
    def fill_subscription_email(self, email: str):
        self.fill_text(self.__SUBSCRIPTION_EMAIL__, email)

    @allure.step("Click subscribe button")
    def click_subscribe_button(self):
        self.click(self.__SUBSCRIPTION_BUTTON__)

    @allure.step("Subscribe with email {email}")
    def subscribe(self, email: str):
        self.fill_subscription_email(email)
        self.click_subscribe_button()

    @allure.step("Check that subscription success message appeared")
    def is_subscribe_success_visible(self, timeout: int = 3000) -> bool:
        # call right after subscribe() - the message hides again after ~1.5 seconds
        try:
            self.page.locator(self.__SUBSCRIBE_SUCCESS__).wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_validation_message_on_field(self) -> str:
        return self.get_validation_message(self.__SUBSCRIPTION_EMAIL__)