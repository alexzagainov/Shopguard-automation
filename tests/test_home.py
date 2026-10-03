import time

import pytest

from tests.base_test import BaseTest



class TestHome(BaseTest):

    def test_enter_test_case(self):
        self.home_page.click_testcase_button()
        assert self.home_page.get_page_url()=="https://automationexercise.com/test_cases"

