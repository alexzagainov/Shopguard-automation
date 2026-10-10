import allure

from pages.base_page import BasePage


class PaymentPage(BasePage):
    _NAME_ON_CARD = '[name="name_on_card"]'
    _CARD_NUMBER ='[data-qa="card-number"]'
    _CVC ='[data-qa="cvc"]'
    _EXPIRATION_MONTH ='[data-qa="expiry-month"]'
    _EXPIRATION_YEAR ='[data-qa="expiry-year"]'
    _CONFIRM_BTN ='#submit'
    _PAYMENT_FORM = '#payment-form'
    _SUCCESS_MESSAGE = '#success_message'

    def __init__(self, page):
        super().__init__(page)

    @allure.step("Fill name on card")
    def fill_name_on_card(self,name_on_card):
        self.fill_text(self._NAME_ON_CARD,name_on_card)

    @allure.step("Fill card number")
    def fill_card_number(self,card_number):
        self.fill_text(self._CARD_NUMBER,card_number)

    @allure.step("Fill cvc")
    def fill_cvc(self,cvc):
        self.fill_text(self._CVC,cvc)

    @allure.step("Fill expiration date")
    def fill_expiration_date(self,month,year):
        self.fill_text(self._EXPIRATION_MONTH,month)
        self.fill_text(self._EXPIRATION_YEAR,year)

    def fill_payment(self,name_on_card,card_number,cvc,expiration_month,expiration_year):
        self.fill_name_on_card(name_on_card)
        self.fill_card_number(card_number)
        self.fill_cvc(cvc)
        self.fill_expiration_date(expiration_month,expiration_year)

    @allure.step("Click 'Pay and Confirm Order' and get the success message")
    def confirm_and_get_success_message(self) -> str:
        # the site shows the message on submit and leaves the page at the same moment,
        # so it's gone before Playwright can look - catch it from inside the page instead
        messages = []
        self.page.expose_function("reportSuccessMessage", lambda text: messages.append(text))
        self.page.locator(self._PAYMENT_FORM).evaluate(
            """(form, selector) => form.addEventListener("submit", () => {
                const message = document.querySelector(selector);
                if (message.offsetHeight > 0) window.reportSuccessMessage(message.innerText.trim());
            })""",
            self._SUCCESS_MESSAGE,
        )
        self.click(self._CONFIRM_BTN)
        self.page.wait_for_url("**/payment_done/**")
        # empty string = the message never showed
        return messages[0] if messages else ""

