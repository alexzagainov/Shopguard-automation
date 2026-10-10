import pytest

from models.user import User
from tests.base_test import BaseTest


class TestCart(BaseTest):
    def test_add_one_product_to_cart(self):
        self.header.products()
        expected_name = self.products_list.get_products_names()[0]
        expected_price = self.products_list.get_products_prices()[0]

        self.products_list.add_to_cart(0)
        self.products_list.view_cart()

        names = self.cart_page.get_products_names()
        assert names == [expected_name], f"expected only '{expected_name}' in cart, found {names}"
        assert self.cart_page.get_products_prices() == [expected_price], "wrong price in cart"
        assert self.cart_page.get_products_quantities() == [1], "wrong quantity in cart"
        assert self.cart_page.get_products_totals() == [expected_price], "wrong total in cart"

    @pytest.mark.parametrize("indexes", [
        pytest.param([0, 1], id="2 products"),
        pytest.param([0, 2, 5], id="3 products"),
        pytest.param([3, 7, 10, 20], id="4 products"),
    ])
    def test_add_few_products_to_cart(self, indexes: list):
        self.header.products()
        all_names = self.products_list.get_products_names()
        all_prices = self.products_list.get_products_prices()
        expected_names = [all_names[i] for i in indexes]
        expected_prices = [all_prices[i] for i in indexes]

        for i in indexes[:-1]:
            self.products_list.add_to_cart(i)
            self.products_list.continue_shopping()   # close the "Added!" popup before the next add
        self.products_list.add_to_cart(indexes[-1])
        self.products_list.view_cart()

        names = self.cart_page.get_products_names()
        assert names == expected_names, f"expected {expected_names} in cart, found {names}"
        assert self.cart_page.get_products_prices() == expected_prices, "wrong prices in cart"
        assert self.cart_page.get_products_quantities() == [1] * len(indexes), "wrong quantities in cart"
        # each product was added once, so each row's total equals its price
        assert self.cart_page.get_products_totals() == expected_prices, "wrong totals in cart"

    @pytest.mark.parametrize("times", [
        pytest.param(2, id="2 times"),
        pytest.param(3, id="3 times"),
        pytest.param(5, id="5 times"),
    ])
    def test_add_same_product_few_times(self, times: int):
        self.header.products()
        expected_name = self.products_list.get_products_names()[0]
        expected_price = self.products_list.get_products_prices()[0]

        for _ in range(times - 1):
            self.products_list.add_to_cart(0)
            self.products_list.continue_shopping()   # close the "Added!" popup before the next add
        self.products_list.add_to_cart(0)
        self.products_list.view_cart()

        # the same product is one row with a bigger quantity, not several rows
        names = self.cart_page.get_products_names()
        assert names == [expected_name], f"expected one row of '{expected_name}' in cart, found {names}"
        assert self.cart_page.get_products_prices() == [expected_price], "wrong price in cart"
        assert self.cart_page.get_products_quantities() == [times], "wrong quantity in cart"
        assert self.cart_page.get_products_totals() == [expected_price * times], "wrong total in cart"

    # Test Case 17
    def test_remove_product_from_cart(self):
        assert self.home_page.get_page_url() == "https://automationexercise.com/", "home page is not displayed"
        all_names = self.products_list.get_products_names()
        for i in [0, 1]:
            self.products_list.add_to_cart(i)
            self.products_list.continue_shopping()
        self.header.cart()
        assert self.cart_page.get_page_url().endswith("/view_cart"), "cart page is not displayed"

        self.cart_page.remove_product(0)
        names = self.cart_page.get_products_names()
        assert names == [all_names[1]], f"expected only '{all_names[1]}' left in cart, found {names}"

        self.cart_page.remove_product(0)
        assert self.cart_page.get_products_names() == [], "cart should be empty"
        assert self.cart_page.is_empty_cart_message_visible(), "'Cart is empty!' is not visible"

    # Test Case 20
    def test_search_products_and_verify_cart_after_login(self, registered_user: User):
        keyword = "jeans"
        self.header.products()
        assert self.products_list.get_title() == "All Products"

        self.products_page.search(keyword)
        assert self.products_list.get_title() == "Searched Products"
        found = self.products_list.get_products_names()
        assert len(found) > 0, f"no results for '{keyword}'"
        unrelated = [name for name in found if keyword not in name.lower()]
        assert unrelated == [], f"products not related to '{keyword}': {unrelated}"

        for i in range(len(found)):
            self.products_list.add_to_cart(i)
            self.products_list.continue_shopping()
        self.header.cart()
        names = self.cart_page.get_products_names()
        assert names == found, f"expected {found} in cart before login, found {names}"

        self.header.enter_login_signup_page()
        self.login_page.login(registered_user.email, registered_user.password)
        self.header.cart()
        names = self.cart_page.get_products_names()
        assert names == found, f"expected {found} in cart after login, found {names}"

    # Test Case 22
    def test_add_to_cart_from_recommended_items(self):
        assert self.home_page.is_recommended_items_visible(), "'Recommended Items' are not visible"
        expected_name = self.home_page.get_recommended_name(0)
        self.home_page.add_recommended_to_cart(0)
        self.home_page.view_cart()

        names = self.cart_page.get_products_names()
        assert names == [expected_name], f"expected only '{expected_name}' in cart, found {names}"

