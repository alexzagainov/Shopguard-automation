from models.user import User
from tests.base_test import BaseTest

SUCCESS_MESSAGE = "Your order has been placed successfully!"


class TestCheckout(BaseTest):

    def add_products_to_cart(self, indexes: list) -> tuple:
        # returns the names and prices of the added products, to check them in the order later
        all_names = self.products_list.get_products_names()
        all_prices = self.products_list.get_products_prices()
        for i in indexes:
            self.products_list.add_to_cart(i)
            self.products_list.continue_shopping()
        return [all_names[i] for i in indexes], [all_prices[i] for i in indexes]

    def verify_logged_in(self, user: User):
        assert self.header.get_logged_in_as_username() == f"Logged in as {user.name}"

    def verify_account_created_and_continue(self):
        assert self.sign_up_page.get_account_created_title() == "Account Created!"
        self.sign_up_page.continue_after_create_account()

    def go_to_checkout(self):
        self.header.cart()
        assert self.cart_page.get_page_url().endswith("/view_cart"), "cart page is not displayed"
        self.cart_page.proceed_to_checkout()

    def verify_address(self, user: User):
        # the address the user registered with, the way the checkout page shows it - empty lines are skipped
        expected_address = [line for line in [
            f"{user.title}. {user.first_name} {user.last_name}",
            user.company,
            user.address,
            user.address2,
            f"{user.city} {user.state} {user.zipcode}",
            user.country,
            user.mobile_number,
        ] if line]
        assert self.checkout_page.get_delivery_address() == expected_address, "wrong delivery address"
        assert self.checkout_page.get_billing_address() == expected_address, "wrong billing address"

    def verify_order(self, expected_names: list, expected_prices: list):
        # every product was added once
        names = self.checkout_page.get_products_names()
        assert names == expected_names, f"expected {expected_names} in order, found {names}"
        assert self.checkout_page.get_products_prices() == expected_prices, "wrong prices in order"
        assert self.checkout_page.get_products_quantities() == [1] * len(expected_names), "wrong quantities in order"
        assert self.checkout_page.get_products_totals() == expected_prices, "wrong totals in order"
        assert self.checkout_page.get_total_amount() == sum(expected_prices), "wrong total amount"

    def place_order_and_pay(self, user: User):
        self.checkout_page.enter_comment("Please deliver in the morning")
        self.checkout_page.place_order()
        self.payment_page.fill_payment(user.name, "4111111111111111", "123", "12", "2030")
        message = self.payment_page.confirm_and_get_success_message()
        assert message == SUCCESS_MESSAGE, f"wrong success message: '{message}'"

    def delete_account(self):
        self.header.delete_account()
        assert self.account_deleted_page.get_account_deleted_title() == "Account Deleted!"
        self.account_deleted_page.continue_after_delete_account()

    # Test Case 14
    def test_register_while_checkout(self):
        user = User()
        assert self.home_page.get_page_url() == "https://automationexercise.com/", "home page is not displayed"
        expected_names, expected_prices = self.add_products_to_cart([0, 1, 2])

        self.go_to_checkout()
        self.cart_page.register_login()
        # register a new user in the middle of the checkout
        self.login_page.sign_up(user.name, user.email)
        self.sign_up_page.fill_the_signup_form(user)
        self.sign_up_page.create_account()
        self.verify_account_created_and_continue()
        self.verify_logged_in(user)

        self.go_to_checkout()
        self.verify_address(user)
        self.verify_order(expected_names, expected_prices)
        self.place_order_and_pay(user)
        self.delete_account()

    # Test Case 15
    def test_register_before_checkout(self):
        user = User()
        assert self.home_page.get_page_url() == "https://automationexercise.com/", "home page is not displayed"
        self.sign_up(user)
        self.verify_account_created_and_continue()
        self.verify_logged_in(user)

        expected_names, expected_prices = self.add_products_to_cart([0, 1, 2])
        self.go_to_checkout()
        self.verify_address(user)
        self.verify_order(expected_names, expected_prices)
        self.place_order_and_pay(user)
        self.delete_account()

    # Test Case 16
    def test_login_before_checkout(self, registered_user: User):
        assert self.home_page.get_page_url() == "https://automationexercise.com/", "home page is not displayed"
        self.header.enter_login_signup_page()
        self.login_page.login(registered_user.email, registered_user.password)
        self.verify_logged_in(registered_user)

        expected_names, expected_prices = self.add_products_to_cart([0, 1, 2])
        self.go_to_checkout()
        self.verify_address(registered_user)
        self.verify_order(expected_names, expected_prices)
        self.place_order_and_pay(registered_user)
        self.delete_account()

    # Test Case 23
    def test_address_details_in_checkout(self):
        user = User()
        assert self.home_page.get_page_url() == "https://automationexercise.com/", "home page is not displayed"
        self.sign_up(user)
        self.verify_account_created_and_continue()
        self.verify_logged_in(user)

        self.add_products_to_cart([0])
        self.go_to_checkout()
        self.verify_address(user)
        self.delete_account()
