import allure
import pytest

from tests.base_test import BaseTest

# Chromium's text; Firefox/WebKit word it differently
REQUIRED_MESSAGE = "Please fill out this field."

# how to get to each page where the footer is tested (every test starts on the home page)
PAGES = {
    "home": lambda self: None,
    "cart": lambda self: self.header.cart(),
}


@allure.feature("Subscription")
class TestFooter(BaseTest):

    @allure.title("TC10/TC11: Subscribe on {page_name} page with {email}")
    @pytest.mark.parametrize("page_name", PAGES.keys())
    @pytest.mark.parametrize("email", ["alex@gmail.com", "alex2@gmail.com"])
    def test_subscription(self, page_name: str, email: str):
        PAGES[page_name](self)
        self.footer.subscribe(email)
        assert self.footer.is_subscribe_success_visible(), "subscription success message did not appear"

    @allure.title("Subscription validation on {page_name} page: {expected}")
    @pytest.mark.parametrize("page_name", PAGES.keys())
    @pytest.mark.parametrize("email,expected", [
        pytest.param("", REQUIRED_MESSAGE, id="empty"),
        pytest.param("alex", "Please include an '@' in the email address. 'alex' is missing an '@'.", id="without @"),
    ])
    def test_subscription_validation(self, page_name: str, email: str, expected: str):
        PAGES[page_name](self)
        self.footer.subscribe(email)
        assert self.footer.get_validation_message_on_field() == expected
