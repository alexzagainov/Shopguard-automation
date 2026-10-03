import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components.cart_modal import CartModal


class ProductDetailsPage(BasePage):
    # the details have no classes - they are plain <p> tags, so they are found by their text
    __PRODUCT_NAME__ = '.product-information h2'
    __CATEGORY__ = ".product-information p:has-text('Category:')"
    __PRICE__ = '.product-information span span'
    __AVAILABILITY__ = ".product-information p:has(b:text-is('Availability:'))"
    __CONDITION__ = ".product-information p:has(b:text-is('Condition:'))"
    __BRAND__ = ".product-information p:has(b:text-is('Brand:'))"
    __QUANTITY__ = '#quantity'
    __ADD_TO_CART__ = '.product-information button.cart'

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
        self.cart_modal = CartModal(page)

    @allure.step("Get product name")
    def get_name(self) -> str:
        return self.get_text(self.__PRODUCT_NAME__)

    @allure.step("Check that {detail} is visible")
    def is_detail_visible(self, detail: str) -> bool:
        return self.page.locator(self.__DETAILS__[detail]).is_visible()

    @allure.step("Check that all product details are visible")
    def is_details_visible(self) -> bool:
        return all(self.is_detail_visible(detail) for detail in self.__DETAILS__)

    @allure.step("Get product price")
    def get_price(self) -> int:
        return self.price_to_int(self.get_text(self.__PRICE__))

    @allure.step("Add product to cart with quantity {quantity}")
    def add_to_cart(self, quantity: int = 1):
        self.fill_text(self.__QUANTITY__, str(quantity))
        self.click(self.__ADD_TO_CART__)
        self.cart_modal.wait_until_open()

    def continue_shopping(self):
        self.cart_modal.continue_shopping()

    def view_cart(self):
        self.cart_modal.view_cart()
