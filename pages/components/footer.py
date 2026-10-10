import allure

from pages.base_page import BasePage


class Footer(BasePage):
    _SUBSCRIPTION_TITLE = ".single-widget h2"
    _SUBSCRIPTION_EMAIL ="#susbscribe_email"   # the site really spells it "susbscribe"
    _SUBSCRIPTION_BUTTON = "#subscribe"
    # always in the HTML but hidden - it's shown for ~1.5 seconds after subscribing
    _SUBSCRIBE_SUCCESS = "#success-subscribe"

    @allure.step("Get subscription title")
    def get_subscription_title(self) -> str:
        # text_content = the text in the HTML, not affected by CSS uppercase
        return self.page.locator(self._SUBSCRIPTION_TITLE).text_content().strip()

    @allure.step("Check that subscription title is on the screen")
    def is_subscription_title_in_viewport(self) -> bool:
        return self.is_in_viewport(self._SUBSCRIPTION_TITLE)

    @allure.step("Fill subscription email: {email}")
    def fill_subscription_email(self, email: str):
        self.fill_text(self._SUBSCRIPTION_EMAIL, email)

    @allure.step("Click subscribe button")
    def click_subscribe_button(self):
        self.click(self._SUBSCRIPTION_BUTTON)

    @allure.step("Subscribe with email {email}")
    def subscribe(self, email: str):
        self.fill_subscription_email(email)
        self.click_subscribe_button()

    @allure.step("Check that subscription success message appeared")
    def is_subscribe_success_visible(self, timeout: int = 3000) -> bool:
        # call right after subscribe() - the message hides again after ~1.5 seconds
        return self.is_visible(self._SUBSCRIBE_SUCCESS, timeout)

    def get_validation_message_on_field(self) -> str:
        return self.get_validation_message(self._SUBSCRIPTION_EMAIL)