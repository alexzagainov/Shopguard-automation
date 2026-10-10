import re
from typing import Dict

import allure
import pytest

from models.user import User
from pages.base_page import BasePage

AD_URLS = re.compile(r"googlesyndication|doubleclick|googleads|adservice|google-analytics|googletagmanager|fundingchoices")


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: Dict) -> Dict:
    return {**browser_type_launch_args}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: Dict) -> Dict:
    return {**browser_context_args,
            "viewport": {"width": 1024, "height": 768},
}


@pytest.fixture(scope="function", autouse=True)
def setup_page_function(request, page):
    BasePage.highlight = request.config.getoption("--headed")

    # block ads: they slow down page loads and can cover buttons
    page.route(AD_URLS, lambda route: route.abort())
    # "/" = the base_url from pytest.ini
    page.goto("/", wait_until="domcontentloaded")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # when a test fails, attach what the browser showed to the Allure report
    outcome = yield
    report = outcome.get_result()
    page = item.funcargs.get("page")
    if report.when == "call" and report.failed and page is not None:
        allure.attach(page.screenshot(full_page=True), name="screenshot on failure",
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(page.url, name="url on failure", attachment_type=allure.attachment_type.TEXT)


@pytest.fixture
def registered_user(page, base_url) -> User:
    # a user that already exists before the test - created through the site's API, not the UI
    user = User()
    response = page.request.post(f"{base_url}/api/createAccount", form={
        "name": user.name, "email": user.email, "password": user.password, "title": user.title,
        "birth_date": user.day_of_birth, "birth_month": user.month_of_birth, "birth_year": user.year_of_birth,
        "firstname": user.first_name, "lastname": user.last_name, "company": user.company,
        "address1": user.address, "address2": user.address2, "country": user.country,
        "state": user.state, "city": user.city, "zipcode": user.zipcode, "mobile_number": user.mobile_number,
    })
    # the API always answers HTTP 200 - the real result is in the JSON
    assert response.json()["responseCode"] == 201, f"could not create user: {response.text()}"
    yield user
    # runs also when the test fails; if the test already deleted the account the API answers 404 - that's fine
    page.request.delete(f"{base_url}/api/deleteAccount", form={"email": user.email, "password": user.password})
