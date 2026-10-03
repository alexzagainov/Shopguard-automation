import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    # one row per product in the cart table
    __PRODUCT_NAMES__ = '#cart_info_table .cart_description h4'
    __PRODUCT_PRICES__ = '#cart_info_table .cart_price p'
    __PRODUCT_QUANTITIES__ = '#cart_info_table .cart_quantity button'
    __PRODUCT_TOTALS__ = '#cart_info_table .cart_total_price'

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

    def proceed_to_checkout(self):
        return ""



