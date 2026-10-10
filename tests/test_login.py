import allure
import pytest

from models.user import User
from tests.base_test import BaseTest

# Chromium's text; Firefox/WebKit word it differently
REQUIRED_MESSAGE = "Please fill out this field."
WRONG_LOGIN_MESSAGE = "Your email or password is incorrect!"


@allure.feature("Login")
class TestLogin(BaseTest):

    def sign_up_and_logout(self, user: User):
        # a user that exists on the site but is not logged in
        self.sign_up(user)
        self.sign_up_page.continue_after_create_account()
        self.header.logout()

    @allure.title("TC2: Login with correct email and password")
    def test_login_valid(self):
        user = User()
        self.sign_up_and_logout(user)
        self.login_page.login(user.email, user.password)
        assert self.header.get_logged_in_as_username() == f"Logged in as {user.name}"

    @allure.title("TC3: Login with incorrect password")
    def test_login_wrong_password(self):
        user = User()
        self.sign_up_and_logout(user)
        self.login_page.login(user.email, "wrongpassword")
        assert self.login_page.get_sign_in_error_message() == WRONG_LOGIN_MESSAGE

    @allure.title("TC3: Login with email that is not registered")
    def test_login_unregistered_email(self):
        # a new User() email was never signed up
        self.header.enter_login_signup_page()
        self.login_page.login(User().email, "1234567")
        assert self.login_page.get_sign_in_error_message() == WRONG_LOGIN_MESSAGE

    # the browser stops the form before it is sent - no user is needed
    @allure.title("Login form validation: {field} - {expected}")
    @pytest.mark.parametrize("email,password,field,expected", [
        pytest.param("", "", "email", REQUIRED_MESSAGE, id="empty email and password"),
        pytest.param("alex@gmail.com", "", "password", REQUIRED_MESSAGE, id="empty password"),
        pytest.param("alex", "1234567", "email",
                     "Please include an '@' in the email address. 'alex' is missing an '@'.", id="email without @"),
    ])
    def test_login_validation(self, email, password, field, expected):
        self.header.enter_login_signup_page()
        self.login_page.login(email, password)
        assert self.login_page.get_sign_in_validation_message(field) == expected
