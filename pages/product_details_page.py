import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductDetailsPage(BasePage):
    # the details have no classes - they are plain <p> tags, so they are found by their text
    __PRODUCT_NAME__ = '.product-information h2'
    __CATEGORY__ = ".product-information p:has-text('Category:')"
    __PRICE__ = '.product-information span span'
    __AVAILABILITY__ = ".product-information p:has(b:text-is('Availability:'))"
    __CONDITION__ = ".product-information p:has(b:text-is('Condition:'))"
    __BRAND__ = ".product-information p:has(b:text-is('Brand:'))"

    __DETAILS__ = {
        "name": __PRODUCT_NAME__,
        "category": __CATEGORY__,
        "price": __PRICE__,
        "availability": __AVAILABILITY__,
        "condition": __CONDITION__,
        "brand": __BRAND__,
    }


    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Get product name")
    def get_name(self) -> str:
        return self.get_text(self.__PRODUCT_NAME__)

    @allure.step("Check that {detail} is visible")
    def is_detail_visible(self, detail: str) -> bool:
        return self.page.locator(self.__DETAILS__[detail]).is_visible()

    @allure.step("Check that all product details are visible")
    def is_details_visible(self) -> bool:
        return all(self.is_detail_visible(detail) for detail in self.__DETAILS__)