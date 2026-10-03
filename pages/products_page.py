import re

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductsPage(BasePage):
    __SEARCH_BAR__ = '[name="search"]'
    __SUBMIT_SEARCH_BUTTON__ = '#submit_search'
    # one card per product: holds the name/price and the "View Product" link
    __PRODUCT_CARDS__ = '.features_items .product-image-wrapper'
    __PRODUCT_NAME__ = '.productinfo p'
    __VIEW_PRODUCT__ = "a:has-text('View Product')"

    def __init__(self, page:Page):
        super().__init__(page)

    @allure.step("Search for {keyword}")
    def search(self, keyword:str):
        self.fill_text(self.__SEARCH_BAR__, keyword)
        self.click(self.__SUBMIT_SEARCH_BUTTON__)
        # the search loads a new page (/products?search=...) - wait for it before reading the results
        self.page.wait_for_url(re.compile(r"/products\?search="), wait_until="load")

    @allure.step("Get products names")
    def get_products_names(self) -> list:
        return self.page.locator(self.__PRODUCT_CARDS__).locator(self.__PRODUCT_NAME__).all_text_contents()

    @allure.step("Click 'View Product' of product number {index}")
    def view_product(self, index: int = 0):
        # look for the link only inside this card - every card has its own "View Product"
        card = self.page.locator(self.__PRODUCT_CARDS__).nth(index)
        card.locator(self.__VIEW_PRODUCT__).click()
        self.page.wait_for_url("**/product_details/**", wait_until="load")

