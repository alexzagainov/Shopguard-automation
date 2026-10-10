import re
from typing import Dict
import pytest

from models.user import User
from pages.account_deleted_page import AccountDeletedPage
from pages.base_page import BasePage
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

API_URL = "https://automationexercise.com/api"
AD_URLS = re.compile(r"googlesyndication|doubleclick|googleads|adservice|google-analytics|googletagmanager|fundingchoices")


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: Dict) -> Dict:
    return {**browser_type_launch_args}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: Dict) -> Dict:
    return {**browser_context_args,
            "viewport": {"width": 1024, "height": 768},
}


@pytest.fixture(scope="function", autouse=True)
def setup_page_function(request, page):
    BasePage.highlight = request.config.getoption("--headed")

    # block ads: they slow down page loads and can cover buttons
    page.route(AD_URLS, lambda route: route.abort())
    page.goto("https://automationexercise.com", wait_until="domcontentloaded")

    # only attach to the class if the test is inside a class
    if request.cls is not None:
        request.cls.page = page
        request.cls.login_page = LoginPage(page)
        request.cls.sign_up_page = SignUpPage(page)
        request.cls.contact_us_page = ContactUsPage(page)
        request.cls.header =Header(page)
        request.cls.footer = Footer(page)
        request.cls.products_list = ProductsList(page)
        request.cls.sidebar = Sidebar(page)
        request.cls.home_page = HomePage(page)
        request.cls.products_page = ProductsPage(page)
        request.cls.product_details_page = ProductDetailsPage(page)
        request.cls.cart_page = CartPage(page)
        request.cls.checkout_page = CheckoutPage(page)
        request.cls.account_deleted_page = AccountDeletedPage(page)
        request.cls.payment_page = PaymentPage(page)


@pytest.fixture
def registered_user(page) -> User:
    # a user that already exists before the test - created through the site's API, not the UI
    user = User()
    response = page.request.post(f"{API_URL}/createAccount", form={
        "name": user.name, "email": user.email, "password": user.password, "title": user.title,
        "birth_date": user.day_of_birth, "birth_month": user.month_of_birth, "birth_year": user.year_of_birth,
        "firstname": user.first_name, "lastname": user.last_name, "company": user.company,
        "address1": user.address, "address2": user.address2, "country": user.country,
        "state": user.state, "city": user.city, "zipcode": user.zipcode, "mobile_number": user.mobile_number,
    })
    # the API always answers HTTP 200 - the real result is in the JSON
    assert response.json()["responseCode"] == 201, f"could not create user: {response.text()}"
    yield user
    # runs also when the test fails; if the test already deleted the account the API answers 404 - that's fine
    page.request.delete(f"{API_URL}/deleteAccount", form={"email": user.email, "password": user.password})
