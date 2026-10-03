import allure

from pages.base_page import BasePage


class CartModal(BasePage):
    # the "Added!" popup - opens after "Add to cart" from the products list AND from the product details page
    __CART_MODAL__ = '#cartModal'
    __CONTINUE_SHOPPING__ = "#cartModal button:has-text('Continue Shopping')"
    __VIEW_CART__ = "#cartModal a:has-text('View Cart')"

    def wait_until_open(self):
        # the popup blocks the page until it's closed
        self.page.locator(self.__CART_MODAL__).wait_for(state="visible")

    @allure.step("Click 'Continue Shopping' in the popup")
    def continue_shopping(self):
        self.click(self.__CONTINUE_SHOPPING__)
        self.page.locator(self.__CART_MODAL__).wait_for(state="hidden")

    @allure.step("Click 'View Cart' in the popup")
    def view_cart(self):
        self.click(self.__VIEW_CART__)
        self.page.wait_for_url("**/view_cart", wait_until="load")
