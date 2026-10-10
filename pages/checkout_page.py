import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    # address lines without the "Your delivery/billing address" title
    __DELIVERY_ADDRESS__ = '#address_delivery li:not(.address_title)'
    __BILLING_ADDRESS__ = '#address_invoice li:not(.address_title)'
    # "Review Your Order" table - one row per product, plus a last row with the total amount
    __PRODUCT_NAMES__ = '#cart_info tr[id^="product-"] .cart_description h4'
    __PRODUCT_PRICES__ = '#cart_info tr[id^="product-"] .cart_price p'
    __PRODUCT_QUANTITIES__ = '#cart_info tr[id^="product-"] .cart_quantity button'
    __PRODUCT_TOTALS__ = '#cart_info tr[id^="product-"] .cart_total_price'
    __TOTAL_AMOUNT__ = '#cart_info tr:last-child .cart_total_price'
    __COMMENT__ = 'textarea[name="message"]'
    __PLACE_ORDER__ = "a:has-text('Place Order')"

    def __init__(self, page: Page):
        super().__init__(page)

    def get_address_lines(self, locator: str) -> list:
        # empty lines (e.g. no company) are skipped, "Netanya Israel\n4237676" -> "Netanya Israel 4237676"
        lines = [" ".join(line.split()) for line in self.page.locator(locator).all_text_contents()]
        return [line for line in lines if line]

    @allure.step("Get delivery address")
    def get_delivery_address(self) -> list:
        return self.get_address_lines(self.__DELIVERY_ADDRESS__)

    @allure.step("Get billing address")
    def get_billing_address(self) -> list:
        return self.get_address_lines(self.__BILLING_ADDRESS__)

    @allure.step("Get products names in order")
    def get_products_names(self) -> list:
        return [name.strip() for name in self.page.locator(self.__PRODUCT_NAMES__).all_text_contents()]

    @allure.step("Get products prices in order")
    def get_products_prices(self) -> list:
        return [self.price_to_int(price) for price in self.page.locator(self.__PRODUCT_PRICES__).all_text_contents()]

    @allure.step("Get products quantities in order")
    def get_products_quantities(self) -> list:
        return [int(quantity) for quantity in self.page.locator(self.__PRODUCT_QUANTITIES__).all_text_contents()]

    @allure.step("Get products total prices in order")
    def get_products_totals(self) -> list:
        return [self.price_to_int(total) for total in self.page.locator(self.__PRODUCT_TOTALS__).all_text_contents()]

    @allure.step("Get order total amount")
    def get_total_amount(self) -> int:
        return self.price_to_int(self.get_text(self.__TOTAL_AMOUNT__))

    @allure.step("Enter comment")
    def enter_comment(self, comment: str):
        self.fill_text(self.__COMMENT__, comment)

    @allure.step("Click 'Place Order'")
    def place_order(self):
        self.click(self.__PLACE_ORDER__)
        self.page.wait_for_url("**/payment")
