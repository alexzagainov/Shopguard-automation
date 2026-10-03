import pytest

from tests.base_test import BaseTest

# how to get to each page where the footer is tested (every test starts on the home page)
PAGES = {
    "home": lambda self: None,
    "cart": lambda self: self.header.cart(),
}


class TestFooter(BaseTest):
    ERROR_MESSAGE_1 = "Please fill out this field."

    @pytest.mark.parametrize("page_name", PAGES.keys())
    @pytest.mark.parametrize("email,wrong_email",[
        pytest.param("alex@gmail.com",False,id="alex@gmail"),
        pytest.param("alex2@gmail.com",False,id="alex2@gmail.com"),
        pytest.param("alex",True,id="alex"),
        pytest.param("",True,id="empty"),])
    def test_subscription(self,page_name:str,email:str,wrong_email:bool):
        PAGES[page_name](self)
        self.footer.subscribe(email)
        if wrong_email:
            if email == "":
                assert self.footer.get_validation_message_on_field() == self.ERROR_MESSAGE_1
            else:
                assert self.footer.get_validation_message_on_field() == f"Please include an '@' in the email address. '{email}' is missing an '@'."
        else:
            assert self.footer.is_subscribe_success_visible()