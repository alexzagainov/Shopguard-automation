import allure

from pages.base_page import BasePage


class CartModal(BasePage):
    # the "Added!" popup - opens after "Add to cart" from the products list AND from the product details page
    _CART_MODAL = '#cartModal'
    _CONTINUE_SHOPPING = "#cartModal button:has-text('Continue Shopping')"
    _VIEW_CART = "#cartModal a:has-text('View Cart')"

    def wait_until_open(self):
        # the popup blocks the page until it's closed
        self.page.locator(self._CART_MODAL).wait_for(state="visible")

    @allure.step("Click 'Continue Shopping' in the popup")
    def continue_shopping(self):
        self.click(self._CONTINUE_SHOPPING)
        self.page.locator(self._CART_MODAL).wait_for(state="hidden")

    @allure.step("Click 'View Cart' in the popup")
    def view_cart(self):
        self.click(self._VIEW_CART)
        self.page.wait_for_url("**/view_cart", wait_until="load")
