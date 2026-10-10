import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    # one row per product in the cart table
    _PRODUCT_NAMES = '#cart_info_table .cart_description h4'
    _PRODUCT_PRICES = '#cart_info_table .cart_price p'
    _PRODUCT_QUANTITIES = '#cart_info_table .cart_quantity button'
    _PRODUCT_TOTALS = '#cart_info_table .cart_total_price'
    _REMOVE_PRODUCT = '#cart_info_table .cart_quantity_delete'
    _PRODUCT_ROWS = '#cart_info_table tbody tr'
    _EMPTY_CART = '#empty_cart'
    _PROCEED_TO_CHECKOUT ="a:has-text('Proceed To Checkout')"
    # the "Checkout" popup - opens on "Proceed To Checkout" when not logged in
    _REGISTER_LOGIN = '#checkoutModal a[href="/login"]'

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Get products names in cart")
    def get_products_names(self) -> list:
        # empty list = empty cart
        return [name.strip() for name in self.page.locator(self._PRODUCT_NAMES).all_text_contents()]

    @allure.step("Get products prices in cart")
    def get_products_prices(self) -> list:
        return [self.price_to_int(price) for price in self.page.locator(self._PRODUCT_PRICES).all_text_contents()]

    @allure.step("Get products quantities in cart")
    def get_products_quantities(self) -> list:
        return [int(quantity) for quantity in self.page.locator(self._PRODUCT_QUANTITIES).all_text_contents()]

    @allure.step("Get products total prices in cart")
    def get_products_totals(self) -> list:
        return [self.price_to_int(total) for total in self.page.locator(self._PRODUCT_TOTALS).all_text_contents()]

    @allure.step("Click 'X' of product number {index}")
    def remove_product(self, index: int = 0):
        rows = self.page.locator(self._PRODUCT_ROWS)
        count_before = rows.count()
        self.page.locator(self._REMOVE_PRODUCT).nth(index).click()
        # the row is removed by the site's JS after the server answers - wait for it
        self.page.wait_for_function(
            "([selector, count]) => document.querySelectorAll(selector).length < count",
            arg=[self._PRODUCT_ROWS, count_before],
        )

    @allure.step("Check that 'Cart is empty!' is visible")
    def is_empty_cart_message_visible(self) -> bool:
        return self.is_visible(self._EMPTY_CART)

    @allure.step("Click 'Proceed To Checkout'")
    def proceed_to_checkout(self):
        self.click(self._PROCEED_TO_CHECKOUT)

    @allure.step("Click 'Register / Login' in the checkout popup")
    def register_login(self):
        self.click(self._REGISTER_LOGIN)
        self.page.wait_for_url("**/login")

    



