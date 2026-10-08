import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.web


@pytest.mark.smoke
def test_inventory_lists_all_products(logged_in_page, app_url):
    inventory = InventoryPage(logged_in_page, app_url)
    expect(inventory.products).to_have_count(4)


def test_cart_badge_counts_every_item_added(logged_in_page, app_url):
    inventory = InventoryPage(logged_in_page, app_url)
    expect(inventory.cart_count).to_have_text("0")
    inventory.add_to_cart(1).add_to_cart(3, times=2)
    expect(inventory.cart_count).to_have_text("3")


def test_cart_shows_quantities_and_subtotal(logged_in_page, app_url):
    inventory = InventoryPage(logged_in_page, app_url)
    inventory.add_to_cart(1, times=2).add_to_cart(2)
    inventory.go_to_cart()

    cart = CartPage(logged_in_page, app_url)
    expect(cart.quantity(1)).to_have_text("2")
    expect(cart.quantity(2)).to_have_text("1")
    # 2 x 79.99 + 49.50 = 209.48
    expect(cart.subtotal).to_have_text("$209.48")


def test_removing_last_item_empties_cart_and_disables_checkout(logged_in_page, app_url):
    InventoryPage(logged_in_page, app_url).add_to_cart(4).go_to_cart()

    cart = CartPage(logged_in_page, app_url)
    cart.remove(4)
    expect(cart.empty_message).to_be_visible()
    expect(cart.checkout_button).to_be_disabled()
    expect(cart.subtotal).to_have_text("$0.00")
