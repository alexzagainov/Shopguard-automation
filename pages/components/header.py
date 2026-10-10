import re
import allure

from pages.base_page import BasePage


class Header(BasePage):
    _LOGIN_SIGNUP_TITLE= ".fa.fa-lock"
    _LOGGED_IN_AS_TXT='a:has(.fa-user)'
    _LOGOUT='a:has(.fa-lock)'
    _DELETE_ACCOUNT='a:has(.fa-trash-o)'
    _PRODUCTS= 'a:has(.material-icons.card_travel)'
    _CART= 'li>a>.fa.fa-shopping-cart'
    _CONTACT_US= '.fa.fa-envelope'
    _HOME= 'a:has(.fa-home)'

    def navigate(self, locator: str, url_ending: str):
        self.click(locator)
        # wait until the new page and its scripts are loaded, otherwise the test acts before the site's JS is ready
        self.page.wait_for_url(re.compile(url_ending + "$"), wait_until="load")

    @allure.step("Go to 'Signup / Login' page")
    def enter_login_signup_page(self):
        self.navigate(self._LOGIN_SIGNUP_TITLE, "/login")


    @allure.step("Logout")
    def logout(self):
        # /logout redirects to /login
        self.navigate(self._LOGOUT, "/login")

    @allure.step("Delete account")
    def delete_account(self):
        self.navigate(self._DELETE_ACCOUNT, "/delete_account")

    @allure.step("Go to Home page")
    def home_page(self):
        # the site root - an address with nothing after the domain
        self.navigate(self._HOME, "://[^/]+/")

    @allure.step("Go to Products page")
    def products(self):
        self.navigate(self._PRODUCTS, "/products")

    @allure.step("Go to Cart page")
    def cart(self):
        self.navigate(self._CART, "/view_cart")

    @allure.step("Go to Contact Us page")
    def contact_us(self):
        self.navigate(self._CONTACT_US, "/contact_us")

    @allure.step("Get 'Logged in as' text")
    def get_logged_in_as_username(self):
        # the link text starts with a space after the user icon
        return self.get_text(self._LOGGED_IN_AS_TXT).strip()
