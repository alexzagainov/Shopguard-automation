import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    # one row per product in the cart table
    __PRODUCT_NAMES__ = '#cart_info_table .cart_description h4'
    __PRODUCT_PRICES__ = '#cart_info_table .cart_price p'
    __PRODUCT_QUANTITIES__ = '#cart_info_table .cart_quantity button'
    __PRODUCT_TOTALS__ = '#cart_info_table .cart_total_price'
    __REMOVE_PRODUCT__ = '#cart_info_table .cart_quantity_delete'
    __PRODUCT_ROWS__ = '#cart_info_table tbody tr'
    __EMPTY_CART__ = '#empty_cart'
    __PROCEED_TO_CHECKOUT__ ="a:has-text('Proceed To Checkout')"
    # the "Checkout" popup - opens on "Proceed To Checkout" when not logged in
    __REGISTER_LOGIN__ = '#checkoutModal a[href="/login"]'

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Get products names in cart")
    def get_products_names(self) -> list:
        # empty list = empty cart
        return [name.strip() for name in self.page.locator(self.__PRODUCT_NAMES__).all_text_contents()]

    @allure.step("Get products prices in cart")
    def get_products_prices(self) -> list:
        return [self.price_to_int(price) for price in self.page.locator(self.__PRODUCT_PRICES__).all_text_contents()]

    @allure.step("Get products quantities in cart")
    def get_products_quantities(self) -> list:
        return [int(quantity) for quantity in self.page.locator(self.__PRODUCT_QUANTITIES__).all_text_contents()]

    @allure.step("Get products total prices in cart")
    def get_products_totals(self) -> list:
        return [self.price_to_int(total) for total in self.page.locator(self.__PRODUCT_TOTALS__).all_text_contents()]

    @allure.step("Click 'X' of product number {index}")
    def remove_product(self, index: int = 0):
        rows = self.page.locator(self.__PRODUCT_ROWS__)
        count_before = rows.count()
        self.page.locator(self.__REMOVE_PRODUCT__).nth(index).click()
        # the row is removed by the site's JS after the server answers - wait for it
        self.page.wait_for_function(
            "([selector, count]) => document.querySelectorAll(selector).length < count",
            arg=[self.__PRODUCT_ROWS__, count_before],
        )

    @allure.step("Check that 'Cart is empty!' is visible")
    def is_empty_cart_message_visible(self) -> bool:
        return self.page.locator(self.__EMPTY_CART__).is_visible()

    @allure.step("Click 'Proceed To Checkout'")
    def proceed_to_checkout(self):
        self.click(self.__PROCEED_TO_CHECKOUT__)

    @allure.step("Click 'Register / Login' in the checkout popup")
    def register_login(self):
        self.click(self.__REGISTER_LOGIN__)
        self.page.wait_for_url("**/login")

    



