import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components.cart_modal import CartModal


class HomePage(BasePage):

    # the slider has 3 slides, each with its own button - only the current slide's button is visible
    __TEST_CASE_BUTTONS__ ='.test_cases_list:visible'
    # every slide has the same title - check the one on the current slide
    __SLIDER_TITLE__ = '#slider-carousel .item.active h2'
    __SCROLL_UP_ARROW__ = '#scrollUp'
    __RECOMMENDED_ITEMS__ = '.recommended_items'
    __RECOMMENDED_CAROUSEL__ = '#recommended-item-carousel'
    # the carousel shows 3 of the 6 products at a time - use the ones on the current slide
    __RECOMMENDED_CARDS__ = '.recommended_items .item.active .product-image-wrapper'
    __RECOMMENDED_NAME__ = '.productinfo p'
    __RECOMMENDED_ADD_TO_CART__ = '.productinfo a.add-to-cart'

    def __init__(self,page:Page):
        super().__init__(page)
        self.cart_modal = CartModal(page)

    @allure.step("Click 'Test Cases' button in the slider")
    def click_testcase_button(self):
        self.click(self.__TEST_CASE_BUTTONS__)
        self.page.wait_for_url("**/test_cases", wait_until="load")

    @allure.step("Get slider title")
    def get_slider_title(self) -> str:
        return self.get_text(self.__SLIDER_TITLE__).strip()

    @allure.step("Check that slider title is on the screen")
    def is_slider_title_in_viewport(self, timeout: int = 3000) -> bool:
        return self.is_in_viewport(self.__SLIDER_TITLE__, timeout)

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
        self.click(self.__SCROLL_UP_ARROW__)

    @allure.step("Check that 'Recommended Items' are visible")
    def is_recommended_items_visible(self) -> bool:
        self.page.locator(self.__RECOMMENDED_ITEMS__).scroll_into_view_if_needed()
        return self.page.locator(self.__RECOMMENDED_ITEMS__).is_visible()

    def stop_recommended_carousel(self):
        # the carousel moves to the next slide every few seconds - the mouse over it stops it
        self.page.locator(self.__RECOMMENDED_CAROUSEL__).hover()

    @allure.step("Get name of recommended product number {index}")
    def get_recommended_name(self, index: int = 0) -> str:
        self.stop_recommended_carousel()
        card = self.page.locator(self.__RECOMMENDED_CARDS__).nth(index)
        return card.locator(self.__RECOMMENDED_NAME__).text_content().strip()

    @allure.step("Add recommended product number {index} to cart")
    def add_recommended_to_cart(self, index: int = 0):
        self.stop_recommended_carousel()
        card = self.page.locator(self.__RECOMMENDED_CARDS__).nth(index)
        card.locator(self.__RECOMMENDED_ADD_TO_CART__).click()
        self.cart_modal.wait_until_open()

    def view_cart(self):
        self.cart_modal.view_cart()
