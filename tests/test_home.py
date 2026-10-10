import time

import pytest

from tests.base_test import BaseTest



class TestHome(BaseTest):

    def test_enter_test_case(self):
        self.home_page.click_testcase_button()
        assert self.home_page.get_page_url()=="https://automationexercise.com/test_cases"

    # Test Case 25
    def test_scroll_up_with_arrow(self):
        assert self.home_page.get_page_url() == "https://automationexercise.com/", "home page is not displayed"
        self.home_page.scroll_to_bottom()
        assert self.footer.is_subscription_title_in_viewport(), "'Subscription' is not on the screen"
        assert self.footer.get_subscription_title() == "Subscription"
        # make sure the page really moved, otherwise the check after scrolling up proves nothing
        assert not self.home_page.is_slider_title_in_viewport(timeout=500), "page did not scroll down"

        self.home_page.click_scroll_up_arrow()
        assert self.home_page.is_slider_title_in_viewport(), "page did not scroll up"
        assert self.home_page.get_slider_title() == "Full-Fledged practice website for Automation Engineers"

    # Test Case 26
    def test_scroll_up_without_arrow(self):
        assert self.home_page.get_page_url() == "https://automationexercise.com/", "home page is not displayed"
        self.home_page.scroll_to_bottom()
        assert self.footer.is_subscription_title_in_viewport(), "'Subscription' is not on the screen"
        assert self.footer.get_subscription_title() == "Subscription"
        assert not self.home_page.is_slider_title_in_viewport(timeout=500), "page did not scroll down"

        self.home_page.scroll_to_top()
        assert self.home_page.is_slider_title_in_viewport(), "page did not scroll up"
        assert self.home_page.get_slider_title() == "Full-Fledged practice website for Automation Engineers"

