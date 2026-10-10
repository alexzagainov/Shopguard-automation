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
    login_page: LoginPage
    sign_up_page: SignUpPage
    contact_us_page: ContactUsPage
    header: Header
    footer: Footer
    products_list: ProductsList
    sidebar: Sidebar
    home_page: HomePage
    products_page: ProductsPage
    product_details_page: ProductDetailsPage
    cart_page: CartPage
    checkout_page: CheckoutPage
    account_deleted_page: AccountDeletedPage
    payment_page: PaymentPage

    def sign_up(self, user: User):
        self.header.enter_login_signup_page()
        self.login_page.sign_up(user.name, user.email)
        self.sign_up_page.fill_the_signup_form(user)
        self.sign_up_page.create_account()
