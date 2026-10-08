import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from tests.data_loader import csv_cases

pytestmark = pytest.mark.web


def go_to_checkout(page, app_url):
    InventoryPage(page, app_url).add_to_cart(1).add_to_cart(2).go_to_cart()
    CartPage(page, app_url).checkout()
    return CheckoutPage(page, app_url)


@pytest.mark.parametrize("case", csv_cases("checkout_data.csv"))
def test_checkout_form(logged_in_page, app_url, case):
    checkout = go_to_checkout(logged_in_page, app_url)
    checkout.fill(case["first_name"], case["last_name"], case["zip"]).place_order()

    if case["expected"] == "success":
        expect(checkout.confirmation).to_be_visible()
        expect(checkout.order_id).to_have_text("1001")
        # (79.99 + 49.50) = 129.49, + 8% tax 10.36 = 139.85
        expect(checkout.order_total).to_have_text("$139.85")
    else:
        expect(checkout.error).to_have_text(case["expected"])
        expect(checkout.confirmation).to_be_hidden()


@pytest.mark.smoke
def test_cart_is_empty_after_successful_order(logged_in_page, app_url):
    checkout = go_to_checkout(logged_in_page, app_url)
    checkout.fill("Zalina", "Yusop", "75201").place_order()
    expect(checkout.confirmation).to_be_visible()

    cart = CartPage(logged_in_page, app_url).open()
    expect(cart.empty_message).to_be_visible()
