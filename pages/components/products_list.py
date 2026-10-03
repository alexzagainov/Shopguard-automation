import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components.cart_modal import CartModal


class ProductsList(BasePage):
    # the same product cards appear on home, products, search, category and brand pages
    __PRODUCT_CARDS__ = '.features_items .product-image-wrapper'
    __PRODUCT_NAME__ = '.productinfo p'
    __PRODUCT_PRICE__ = '.productinfo h2'
    __VIEW_PRODUCT__ = "a:has-text('View Product')"
    # each card has 2 "Add to cart" links (one in the card, one in the hover overlay) - use the card's one
    __ADD_TO_CART__ = '.productinfo a.add-to-cart'

    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_modal = CartModal(page)

    @allure.step("Get products names")
    def get_products_names(self) -> list:
        return self.page.locator(self.__PRODUCT_CARDS__).locator(self.__PRODUCT_NAME__).all_text_contents()

    @allure.step("Get products prices")
    def get_products_prices(self) -> list:
        prices = self.page.locator(self.__PRODUCT_CARDS__).locator(self.__PRODUCT_PRICE__).all_text_contents()
        return [self.price_to_int(price) for price in prices]

    @allure.step("Click 'View Product' of product number {index}")
    def view_product(self, index: int = 0):
        # look for the link only inside this card - every card has its own "View Product"
        card = self.page.locator(self.__PRODUCT_CARDS__).nth(index)
        card.locator(self.__VIEW_PRODUCT__).click()
        self.page.wait_for_url("**/product_details/**", wait_until="load")

    @allure.step("Add product number {index} to cart")
    def add_to_cart(self, index: int = 0):
        card = self.page.locator(self.__PRODUCT_CARDS__).nth(index)
        card.locator(self.__ADD_TO_CART__).click()
        self.cart_modal.wait_until_open()

    def continue_shopping(self):
        self.cart_modal.continue_shopping()

    def view_cart(self):
        self.cart_modal.view_cart()
