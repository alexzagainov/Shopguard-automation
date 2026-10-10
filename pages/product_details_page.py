import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components.cart_modal import CartModal


class ProductDetailsPage(BasePage):
    # the details have no classes - they are plain <p> tags, so they are found by their text
    _PRODUCT_NAME = '.product-information h2'
    _CATEGORY = ".product-information p:has-text('Category:')"
    _PRICE = '.product-information span span'
    _AVAILABILITY = ".product-information p:has(b:text-is('Availability:'))"
    _CONDITION = ".product-information p:has(b:text-is('Condition:'))"
    _BRAND = ".product-information p:has(b:text-is('Brand:'))"
    _QUANTITY = '#quantity'
    _ADD_TO_CART = '.product-information button.cart'
    _WRITE_REVIEW_TAB = "a[href='#reviews']"
    _REVIEW_NAME = '#review-form #name'
    _REVIEW_EMAIL = '#review-form #email'
    _REVIEW_TEXT = '#review-form #review'
    _REVIEW_SUBMIT = '#button-review'
    # the outer #review-section has 0 height, so Playwright sees it as hidden - check the alert inside it
    _REVIEW_SUCCESS = '#review-section .alert-success'

    _DETAILS = {
        "name": _PRODUCT_NAME,
        "category": _CATEGORY,
        "price": _PRICE,
        "availability": _AVAILABILITY,
        "condition": _CONDITION,
        "brand": _BRAND,
    }


    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_modal = CartModal(page)

    @allure.step("Get product name")
    def get_name(self) -> str:
        return self.get_text(self._PRODUCT_NAME)

    @allure.step("Check that {detail} is visible")
    def is_detail_visible(self, detail: str) -> bool:
        return self.is_visible(self._DETAILS[detail])

    @allure.step("Check that all product details are visible")
    def is_details_visible(self) -> bool:
        return all(self.is_detail_visible(detail) for detail in self._DETAILS)

    @allure.step("Get product price")
    def get_price(self) -> int:
        return self.price_to_int(self.get_text(self._PRICE))

    @allure.step("Add product to cart with quantity {quantity}")
    def add_to_cart(self, quantity: int = 1):
        self.fill_text(self._QUANTITY, str(quantity))
        self.click(self._ADD_TO_CART)
        self.cart_modal.wait_until_open()

    @allure.step("Check that 'Write Your Review' is visible")
    def is_write_review_visible(self) -> bool:
        return self.is_visible(self._WRITE_REVIEW_TAB)

    @allure.step("Write review as {name}")
    def write_review(self, name: str, email: str, review: str):
        self.fill_text(self._REVIEW_NAME, name)
        self.fill_text(self._REVIEW_EMAIL, email)
        self.fill_text(self._REVIEW_TEXT, review)
        self.click(self._REVIEW_SUBMIT)

    @allure.step("Get review success message")
    def get_review_success_message(self) -> str:
        # call right after write_review() - the message hides again after 2 seconds
        message = self.page.locator(self._REVIEW_SUCCESS)
        message.wait_for(state="visible", timeout=2000)
        return message.inner_text().strip()

    def continue_shopping(self):
        self.cart_modal.continue_shopping()

    def view_cart(self):
        self.cart_modal.view_cart()
