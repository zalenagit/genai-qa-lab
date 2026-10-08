import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from tests.data_loader import json_cases

pytestmark = pytest.mark.web


@pytest.mark.parametrize("case", json_cases("login_users.json"))
def test_login(page, app_url, case):
    LoginPage(page, app_url).open().login(case["username"], case["password"])

    if case["expected"] == "success":
        expect(page).to_have_url(f"{app_url}/inventory.html")
        expect(InventoryPage(page, app_url).heading).to_be_visible()
    else:
        login = LoginPage(page, app_url)
        expect(login.error).to_have_text(case["expected"])
        expect(page).to_have_url(f"{app_url}/index.html")


@pytest.mark.smoke
def test_protected_page_redirects_to_login_when_signed_out(page, app_url):
    InventoryPage(page, app_url).open()
    expect(page).to_have_url(f"{app_url}/index.html")
