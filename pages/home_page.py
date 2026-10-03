import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):

    # the slider has 3 slides, each with its own button - only the current slide's button is visible
    __TEST_CASE_BUTTONS__ ='.test_cases_list:visible'
    def __init__(self,page:Page):
        super().__init__(page)

    @allure.step("Click 'Test Cases' button in the slider")
    def click_testcase_button(self):
        self.click(self.__TEST_CASE_BUTTONS__)
        self.page.wait_for_url("**/test_cases", wait_until="load")

