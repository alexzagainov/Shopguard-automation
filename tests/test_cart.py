import pytest

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



