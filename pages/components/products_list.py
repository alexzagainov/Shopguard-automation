import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components.cart_modal import CartModal


class ProductsList(BasePage):
    # the same product cards appear on home, products, search, category and brand pages
    # "Features Items", "All Products", "Searched Products", "Women - Tops Products", "Brand - Polo Products"
    _TITLE = '.features_items h2.title'
    _PRODUCT_CARDS = '.features_items .product-image-wrapper'
    _PRODUCT_NAME = '.productinfo p'
    _PRODUCT_PRICE = '.productinfo h2'
    _VIEW_PRODUCT = "a:has-text('View Product')"
    # each card has 2 "Add to cart" links (one in the card, one in the hover overlay) - use the card's one
    _ADD_TO_CART = '.productinfo a.add-to-cart'

    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_modal = CartModal(page)

    @allure.step("Get products list title")
    def get_title(self) -> str:
        # text_content = the text in the HTML, not affected by CSS uppercase
        return self.page.locator(self._TITLE).text_content().strip()

    @allure.step("Get products names")
    def get_products_names(self) -> list:
        return self.page.locator(self._PRODUCT_CARDS).locator(self._PRODUCT_NAME).all_text_contents()

    @allure.step("Get products prices")
    def get_products_prices(self) -> list:
        prices = self.page.locator(self._PRODUCT_CARDS).locator(self._PRODUCT_PRICE).all_text_contents()
        return [self.price_to_int(price) for price in prices]

    @allure.step("Click 'View Product' of product number {index}")
    def view_product(self, index: int = 0):
        # look for the link only inside this card - every card has its own "View Product"
        card = self.page.locator(self._PRODUCT_CARDS).nth(index)
        card.locator(self._VIEW_PRODUCT).click()
        self.page.wait_for_url("**/product_details/**", wait_until="load")

    @allure.step("Add product number {index} to cart")
    def add_to_cart(self, index: int = 0):
        card = self.page.locator(self._PRODUCT_CARDS).nth(index)
        card.locator(self._ADD_TO_CART).click()
        self.cart_modal.wait_until_open()

    def continue_shopping(self):
        self.cart_modal.continue_shopping()

    def view_cart(self):
        self.cart_modal.view_cart()
