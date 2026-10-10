import re

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class Sidebar(BasePage):
    # the left side bar - on home, products, category and brand pages
    __CATEGORIES__ = '#accordian'
    # 'Women', 'Men', 'Kids' - clicking one opens its list of sub-categories
    __CATEGORY__ = "#accordian .panel-title a[href='#{category}']"
    __SUB_CATEGORY__ = "#{category} a:has-text('{sub_category}')"
    __BRANDS__ = '.brands_products'
    __BRAND_LINKS__ = '.brands-name a'
    __BRAND__ = '.brands-name a[href="/brand_products/{brand}"]'

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Check that categories are visible")
    def is_categories_visible(self) -> bool:
        return self.page.locator(self.__CATEGORIES__).is_visible()

    @allure.step("Open category {category} -> {sub_category}")
    def open_category(self, category: str, sub_category: str):
        sub_category_link = self.page.locator(self.__SUB_CATEGORY__.format(category=category, sub_category=sub_category))
        # the sub-categories list is closed until the category is clicked
        if not sub_category_link.is_visible():
            self.click(self.__CATEGORY__.format(category=category))
        sub_category_link.click()
        self.page.wait_for_url("**/category_products/**", wait_until="load")

    @allure.step("Check that brands are visible")
    def is_brands_visible(self) -> bool:
        return self.page.locator(self.__BRANDS__).is_visible()

    @allure.step("Get brands and their number of products")
    def get_brands(self) -> dict:
        # "(6)Polo" -> {"Polo": 6}
        brands = {}
        for link in self.page.locator(self.__BRAND_LINKS__).all_text_contents():
            count, name = re.match(r"\s*\((\d+)\)\s*(.+?)\s*$", link).groups()
            brands[name] = int(count)
        return brands

    @allure.step("Open brand {brand}")
    def open_brand(self, brand: str):
        self.click(self.__BRAND__.format(brand=brand))
        self.page.wait_for_url("**/brand_products/**", wait_until="load")
