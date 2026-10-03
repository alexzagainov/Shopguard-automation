from pages.components.footer import Footer
from pages.components.header import Header
from pages.components.products_list import ProductsList
from pages.cart_page import CartPage
from pages.contact_us_page import ContactUsPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
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
    home_page: HomePage
    products_page: ProductsPage
    product_details_page: ProductDetailsPage
    cart_page: CartPage