import re
import allure

from pages.base_page import BasePage


class Header(BasePage):
    __LOGIN_SIGNUP_TITLE__= ".fa.fa-lock"
    __LOGGED_IN_AS_TXT__='a:has(.fa-user)'
    __LOGOUT__='a:has(.fa-lock)'
    __DELETE_ACCOUNT__='a:has(.fa-trash-o)'
    __PRODUCTS__= 'a:has(.material-icons.card_travel)'
    __CART__= 'li>a>.fa.fa-shopping-cart'
    __CONTACT_US__= '.fa.fa-envelope'
    __HOME__= 'a:has(.fa-home)'

    def navigate(self, locator: str, url_ending: str):
        self.click(locator)
        # wait until the new page and its scripts are loaded, otherwise the test acts before the site's JS is ready
        self.page.wait_for_url(re.compile(url_ending + "$"), wait_until="load")

    @allure.step("Go to 'Signup / Login' page")
    def enter_login_signup_page(self):
        self.navigate(self.__LOGIN_SIGNUP_TITLE__, "/login")


    @allure.step("Logout")
    def logout(self):
        # /logout redirects to /login
        self.navigate(self.__LOGOUT__, "/login")

    @allure.step("Delete account")
    def delete_account(self):
        self.navigate(self.__DELETE_ACCOUNT__, "/delete_account")

    @allure.step("Go to Home page")
    def home_page(self):
        self.navigate(self.__HOME__, "automationexercise.com/")

    @allure.step("Go to Products page")
    def products(self):
        self.navigate(self.__PRODUCTS__, "/products")

    @allure.step("Go to Cart page")
    def cart(self):
        self.navigate(self.__CART__, "/view_cart")

    @allure.step("Go to Contact Us page")
    def contact_us(self):
        self.navigate(self.__CONTACT_US__, "/contact_us")

    @allure.step("Get 'Logged in as' text")
    def get_logged_in_as_username(self):
        return self.get_text(self.__LOGGED_IN_AS_TXT__)
