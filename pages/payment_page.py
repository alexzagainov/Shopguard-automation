import allure

from pages.base_page import BasePage


class PaymentPage(BasePage):
    __NAME_ON_CARD__ = '[name="name_on_card"]'
    __CARD_NUMBER__ ='[data-qa="card-number"]'
    __CVC__ ='[data-qa="cvc"]'
    __EXPIRATION_MONTH__ ='[data-qa="expiry-month"]'
    __EXPIRATION_YEAR__ ='[data-qa="expiry-year"]'
    __CONFIRM_BTN__ ='#submit'
    __PAYMENT_FORM__ = '#payment-form'
    __SUCCESS_MESSAGE__ = '#success_message'

    def __init__(self, page):
        super().__init__(page)

    @allure.step("Fill name on card")
    def fill_name_on_card(self,name_on_card):
        self.fill_text(self.__NAME_ON_CARD__,name_on_card)

    @allure.step("Fill card number")
    def fill_card_number(self,card_number):
        self.fill_text(self.__CARD_NUMBER__,card_number)

    @allure.step("Fill cvc")
    def fill_cvc(self,cvc):
        self.fill_text(self.__CVC__,cvc)

    @allure.step("Fill expiration date")
    def fill_expiration_date(self,month,year):
        self.fill_text(self.__EXPIRATION_MONTH__,month)
        self.fill_text(self.__EXPIRATION_YEAR__,year)

    def fill_payment(self,nam_on_card,card_number,cvc,expiration_month,expiration_year):
        self.fill_name_on_card(nam_on_card)
        self.fill_card_number(card_number)
        self.fill_cvc(cvc)
        self.fill_expiration_date(expiration_month,expiration_year)

    @allure.step("Click 'Pay and Confirm Order' and get the success message")
    def confirm_and_get_success_message(self) -> str:
        # the site shows the message on submit and leaves the page at the same moment,
        # so it's gone before Playwright can look - catch it from inside the page instead
        messages = []
        self.page.expose_function("reportSuccessMessage", lambda text: messages.append(text))
        self.page.locator(self.__PAYMENT_FORM__).evaluate(
            """(form, selector) => form.addEventListener("submit", () => {
                const message = document.querySelector(selector);
                if (message.offsetHeight > 0) window.reportSuccessMessage(message.innerText.trim());
            })""",
            self.__SUCCESS_MESSAGE__,
        )
        self.click(self.__CONFIRM_BTN__)
        self.page.wait_for_url("**/payment_done/**")
        # empty string = the message never showed
        return messages[0] if messages else ""

