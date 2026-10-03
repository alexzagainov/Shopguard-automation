from dataclasses import replace

import pytest

from models.user import User
from tests.base_test import BaseTest

# Chromium's text; Firefox/WebKit word it differently
REQUIRED_MESSAGE = "Please fill out this field."


class TestSignUp(BaseTest):

    def sign_up(self, user: User):
        self.header.enter_login_signup_page()
        self.login_page.sign_up(user.name, user.email)
        self.sign_up_page.fill_the_signup_form(user)
        self.sign_up_page.create_account()


    @pytest.mark.parametrize("user", [
        pytest.param(User(title="Mr"), id="mr"),
        pytest.param(User(title="Mrs"), id="mrs"),
        pytest.param(User(newsletter=True, special_offers=True), id="with_checkboxes"),
        pytest.param(User(country="Canada", state="Ontario", city="Toronto"), id="canada"),
        pytest.param(User(day_of_birth="31", month_of_birth="12", year_of_birth="1900"), id="edge_birthdate"),
        pytest.param(User(address2="Apt 5"), id="with_address2"),
    ])
    def test_sign_up(self, user):
        self.sign_up(user)
        assert self.sign_up_page.get_account_created_title() == "Account Created!"



    @pytest.mark.parametrize("field,value", [
        ("title", "Mrs"),
        ("country", "India"),
        ("zipcode", "00000"),
        ("mobile_number", "+972501234567"),
    ])
    def test_sign_up_single_field(self, field, value):
        user = replace(User(), **{field: value})
        self.sign_up(user)
        assert self.sign_up_page.get_account_created_title() == "Account Created!"


    # first step: "New User Signup!" form on the login page
    @pytest.mark.parametrize("field", ["name", "email"])
    def test_unfilled_sign_up_field(self, field):
        user = replace(User(), **{field: ""})
        self.header.enter_login_signup_page()

        self.login_page.sign_up(user.name, user.email)
        assert self.login_page.get_sign_up_validation_message(field) == REQUIRED_MESSAGE
        assert "/login" in self.page.url  # form was not submitted


    # second step: "Enter Account Information" form
    @pytest.mark.parametrize("field", [
        "name", "password", "first_name", "last_name", "address",
        "state", "city", "zipcode", "mobile_number",
    ])
    def test_unfilled_account_field(self, field):
        user = replace(User(), **{field: ""})
        self.header.enter_login_signup_page()
        # the first step needs a valid name, even when testing an empty name on this page
        self.login_page.sign_up(User().name, user.email)
        self.sign_up_page.fill_the_signup_form(user)
        self.sign_up_page.create_account()
        assert self.sign_up_page.get_field_validation_message(field) == REQUIRED_MESSAGE
        assert "/signup" in self.page.url  # form was not submitted

    def test_create_account(self):
        self.sign_up(User())
        self.sign_up_page.continue_after_create_account()
        assert self.header.get_logged_in_as_username()==f" Logged in as {User().name}"


    def test_register_user_with_existing_email(self):
        user = User()
        self.sign_up(user)
        self.sign_up_page.continue_after_create_account()
        self.header.logout()
        self.login_page.sign_up(user.name, user.email)
        assert self.login_page.get_sign_up_error_message() == "Email Address already exist!"





