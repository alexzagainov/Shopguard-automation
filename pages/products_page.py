import re

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductsPage(BasePage):
    _SEARCH_BAR = '[name="search"]'
    _SUBMIT_SEARCH_BUTTON = '#submit_search'
    # the product cards themselves are in components/products_list.py

    def __init__(self, page:Page):
        super().__init__(page)

    @allure.step("Search for {keyword}")
    def search(self, keyword:str):
        self.fill_text(self._SEARCH_BAR, keyword)
        self.click(self._SUBMIT_SEARCH_BUTTON)
        # the search loads a new page (/products?search=...) - wait for it before reading the results
        self.page.wait_for_url(re.compile(r"/products\?search="), wait_until="load")

