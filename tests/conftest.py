import re
from typing import Dict
import pytest

from pages.base_page import BasePage
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
        request.cls.home_page = HomePage(page)
        request.cls.products_page = ProductsPage(page)
        request.cls.product_details_page = ProductDetailsPage(page)
        request.cls.cart_page = CartPage(page)