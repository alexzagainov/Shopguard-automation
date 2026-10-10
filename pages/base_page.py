import re

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect

class BasePage:
    # set from conftest: highlight fields only when running with --headed
    highlight = False

    def __init__(self,page:Page):
        self.page = page


    def fill_text(self, locator: str, text: str, color: str = "yellow"):
        element = self.page.locator(locator)
        if self.highlight:
            element.evaluate(
                """(el, color) => {
                    const origShadow = el.style.boxShadow;
                    const origBackground = el.style.backgroundColor;

                    el.style.boxShadow = '0 0 10px 4px rgba(0, 150, 255, 0.7)';
                    el.style.backgroundColor = color;

                    setTimeout(() => {
                        el.style.boxShadow = origShadow;
                        el.style.backgroundColor = origBackground;
                    }, 300);
                }""",
                color,
            )
        element.fill(text)


    def get_text(self,locator: str):
        return self.page.locator(locator).inner_text()


    def click(self, locator: str):
        self.page.locator(locator).click()

    def check(self,locator: str):
        self.page.locator(locator).check()

    def select_option(self,locator: str,option: str):
        self.page.locator(locator).select_option(option)

    def get_validation_message(self, locator: str) -> str:
        # the browser's message for invalid fields, e.g. "Please fill out this field."
        return self.page.locator(locator).evaluate("el => el.validationMessage")

    def is_element_exist(self, locator: str, timeout: int = 3000) -> bool:
        # waits up to timeout (ms) for the element to be in the page, instead of failing after 30s
        try:
            self.page.locator(locator).wait_for(state="attached", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def is_in_viewport(self, locator: str, timeout: int = 3000) -> bool:
        # "on the screen" - is_visible() is True also for elements you have to scroll to
        try:
            expect(self.page.locator(locator)).to_be_in_viewport(timeout=timeout)
            return True
        except AssertionError:
            return False

    def get_page_url(self):
        return self.page.url

    @staticmethod
    def price_to_int(price_text: str) -> int:
        # "Rs. 500" -> 500
        return int(re.sub(r"\D", "", price_text))
