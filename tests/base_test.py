import pytest
from playwright.sync_api import Page

from models.user import User
from pages.account_deleted_page import AccountDeletedPage
from pages.components.footer import Footer
from pages.components.header import Header
from pages.components.products_list import ProductsList
from pages.components.sidebar import Sidebar
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.contact_us_page import ContactUsPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.payment_page import PaymentPage
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage
from pages.sign_up_page import SignUpPage


class BaseTest:

    # runs before every test of every class that inherits BaseTest - the only place pages are created
    @pytest.fixture(autouse=True)
    def setup_pages(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.login_page = LoginPage(page)
        self.sign_up_page = SignUpPage(page)
        self.contact_us_page = ContactUsPage(page)
        self.header = Header(page)
        self.footer = Footer(page)
        self.products_list = ProductsList(page)
        self.sidebar = Sidebar(page)
        self.home_page = HomePage(page)
        self.products_page = ProductsPage(page)
        self.product_details_page = ProductDetailsPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)
        self.account_deleted_page = AccountDeletedPage(page)
        self.payment_page = PaymentPage(page)

    def sign_up(self, user: User):
        self.header.enter_login_signup_page()
        self.login_page.sign_up(user.name, user.email)
        self.sign_up_page.fill_the_signup_form(user)
        self.sign_up_page.create_account()
