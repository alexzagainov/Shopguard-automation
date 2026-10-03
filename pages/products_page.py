import re

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductsPage(BasePage):
    __SEARCH_BAR__ = '[name="search"]'
    __SUBMIT_SEARCH_BUTTON__ = '#submit_search'
    # the product cards themselves are in components/products_list.py

    def __init__(self, page:Page):
        super().__init__(page)

    @allure.step("Search for {keyword}")
    def search(self, keyword:str):
        self.fill_text(self.__SEARCH_BAR__, keyword)
        self.click(self.__SUBMIT_SEARCH_BUTTON__)
        # the search loads a new page (/products?search=...) - wait for it before reading the results
        self.page.wait_for_url(re.compile(r"/products\?search="), wait_until="load")

