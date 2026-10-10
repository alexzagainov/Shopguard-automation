import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    # address lines without the "Your delivery/billing address" title
    _DELIVERY_ADDRESS = '#address_delivery li:not(.address_title)'
    _BILLING_ADDRESS = '#address_invoice li:not(.address_title)'
    # "Review Your Order" table - one row per product, plus a last row with the total amount
    _PRODUCT_NAMES = '#cart_info tr[id^="product-"] .cart_description h4'
    _PRODUCT_PRICES = '#cart_info tr[id^="product-"] .cart_price p'
    _PRODUCT_QUANTITIES = '#cart_info tr[id^="product-"] .cart_quantity button'
    _PRODUCT_TOTALS = '#cart_info tr[id^="product-"] .cart_total_price'
    _TOTAL_AMOUNT = '#cart_info tr:last-child .cart_total_price'
    _COMMENT = 'textarea[name="message"]'
    _PLACE_ORDER = "a:has-text('Place Order')"

    def __init__(self, page: Page):
        super().__init__(page)

    def get_address_lines(self, locator: str) -> list:
        # empty lines (e.g. no company) are skipped, "Netanya Israel\n4237676" -> "Netanya Israel 4237676"
        lines = [" ".join(line.split()) for line in self.page.locator(locator).all_text_contents()]
        return [line for line in lines if line]

    @allure.step("Get delivery address")
    def get_delivery_address(self) -> list:
        return self.get_address_lines(self._DELIVERY_ADDRESS)

    @allure.step("Get billing address")
    def get_billing_address(self) -> list:
        return self.get_address_lines(self._BILLING_ADDRESS)

    @allure.step("Get products names in order")
    def get_products_names(self) -> list:
        return [name.strip() for name in self.page.locator(self._PRODUCT_NAMES).all_text_contents()]

    @allure.step("Get products prices in order")
    def get_products_prices(self) -> list:
        return [self.price_to_int(price) for price in self.page.locator(self._PRODUCT_PRICES).all_text_contents()]

    @allure.step("Get products quantities in order")
    def get_products_quantities(self) -> list:
        return [int(quantity) for quantity in self.page.locator(self._PRODUCT_QUANTITIES).all_text_contents()]

    @allure.step("Get products total prices in order")
    def get_products_totals(self) -> list:
        return [self.price_to_int(total) for total in self.page.locator(self._PRODUCT_TOTALS).all_text_contents()]

    @allure.step("Get order total amount")
    def get_total_amount(self) -> int:
        return self.price_to_int(self.get_text(self._TOTAL_AMOUNT))

    @allure.step("Enter comment")
    def enter_comment(self, comment: str):
        self.fill_text(self._COMMENT, comment)

    @allure.step("Click 'Place Order'")
    def place_order(self):
        self.click(self._PLACE_ORDER)
        self.page.wait_for_url("**/payment")
