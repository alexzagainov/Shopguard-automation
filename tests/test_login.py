

import pytest

from models.user import User
from tests.base_test import BaseTest


class TestLogin(BaseTest):
    __USERNAME = "username"
    __PASSWORD = "password"



    # VALID = replaced inside the test with the email/password of the user that signed up
    VALID = "VALID"
    users =[pytest.param(VALID,VALID, id="valid"),
            pytest.param("","", id="empty_email_password"),
            pytest.param("alex",VALID, id="wrong_mail_format"),
            pytest.param(VALID,"wrongpassword", id="wrong_password"),
            pytest.param("wrong@gmail.com",VALID, id="wrong_mail"),
            ]
    @pytest.mark.parametrize("email,password",users)
    def test_login(self,email,password):
        user = User()
        if email == self.VALID:
            email = user.email
        if password == self.VALID:
            password = user.password

        self.header.enter_login_signup_page()
        self.login_page.sign_up(user.name,user.email)
        self.sign_up_page.fill_the_signup_form(user)
        self.sign_up_page.create_account()
        self.sign_up_page.continue_after_create_account()
        self.header.logout()


        self.login_page.login(email,password)

        if email == user.email and password == user.password:
            assert self.header.get_logged_in_as_username() == f"Logged in as {user.name}"
        elif email == "" and password == "":
            assert self.login_page.get_sign_in_validation_message("email") == "Please fill out this field."
        elif password == "":
            assert self.login_page.get_sign_in_validation_message("password") == "Please fill out this field."
        elif "@" not in email:
            assert self.login_page.get_sign_in_validation_message("email") == f"Please include an '@' in the email address. '{email}' is missing an '@'."
        elif email == "wrong@gmail.com" or password == "wrongpassword":
            assert self.login_page.get_sign_in_error_message() == "Your email or password is incorrect!"
        else:
            pytest.fail(f"no expected result for email={email!r} password={password!r}")





