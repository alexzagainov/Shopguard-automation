import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components.cart_modal import CartModal


class HomePage(BasePage):

    # the slider has 3 slides, each with its own button - only the current slide's button is visible
    _TEST_CASE_BUTTONS ='.test_cases_list:visible'
    # every slide has the same title - check the one on the current slide
    _SLIDER_TITLE = '#slider-carousel .item.active h2'
    _SCROLL_UP_ARROW = '#scrollUp'
    _RECOMMENDED_ITEMS = '.recommended_items'
    _RECOMMENDED_CAROUSEL = '#recommended-item-carousel'
    # the carousel shows 3 of the 6 products at a time - use the ones on the current slide
    _RECOMMENDED_CARDS = '.recommended_items .item.active .product-image-wrapper'
    _RECOMMENDED_NAME = '.productinfo p'
    _RECOMMENDED_ADD_TO_CART = '.productinfo a.add-to-cart'

    def __init__(self,page:Page):
        super().__init__(page)
        self.cart_modal = CartModal(page)

    @allure.step("Click 'Test Cases' button in the slider")
    def click_testcase_button(self):
        self.click(self._TEST_CASE_BUTTONS)
        self.page.wait_for_url("**/test_cases", wait_until="load")

    @allure.step("Get slider title")
    def get_slider_title(self) -> str:
        return self.get_text(self._SLIDER_TITLE).strip()

    @allure.step("Check that slider title is on the screen")
    def is_slider_title_in_viewport(self, timeout: int = 3000) -> bool:
        return self.is_in_viewport(self._SLIDER_TITLE, timeout)

    @allure.step("Scroll down to the bottom of the page")
    def scroll_to_bottom(self):
        # with the mouse wheel, like a user - more than the page height, so it stops at the bottom
        self.page.mouse.wheel(0, 100000)

    @allure.step("Scroll up to the top of the page")
    def scroll_to_top(self):
        self.page.mouse.wheel(0, -100000)

    @allure.step("Click the arrow at the bottom right to scroll up")
    def click_scroll_up_arrow(self):
        # the arrow appears only after scrolling down
        self.click(self._SCROLL_UP_ARROW)

    @allure.step("Check that 'Recommended Items' are visible")
    def is_recommended_items_visible(self) -> bool:
        self.page.locator(self._RECOMMENDED_ITEMS).scroll_into_view_if_needed()
        return self.is_visible(self._RECOMMENDED_ITEMS)

    def stop_recommended_carousel(self):
        # the carousel moves to the next slide every few seconds - the mouse over it stops it
        self.page.locator(self._RECOMMENDED_CAROUSEL).hover()

    @allure.step("Get name of recommended product number {index}")
    def get_recommended_name(self, index: int = 0) -> str:
        self.stop_recommended_carousel()
        card = self.page.locator(self._RECOMMENDED_CARDS).nth(index)
        return card.locator(self._RECOMMENDED_NAME).text_content().strip()

    @allure.step("Add recommended product number {index} to cart")
    def add_recommended_to_cart(self, index: int = 0):
        self.stop_recommended_carousel()
        card = self.page.locator(self._RECOMMENDED_CARDS).nth(index)
        card.locator(self._RECOMMENDED_ADD_TO_CART).click()
        self.cart_modal.wait_until_open()

    def view_cart(self):
        self.cart_modal.view_cart()
