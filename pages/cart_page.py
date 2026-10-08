from pages.base_page import BasePage


class CartPage(BasePage):
    path = "/cart.html"

    def item(self, product_id: int):
        return self.page.get_by_test_id(f"cart-item-{product_id}")

    def quantity(self, product_id: int):
        return self.item(product_id).locator(".qty")

    @property
    def subtotal(self):
        return self.page.get_by_test_id("subtotal")

    @property
    def empty_message(self):
        return self.page.get_by_text("Your cart is empty.")

    @property
    def checkout_button(self):
        return self.page.get_by_role("button", name="Checkout")

    def remove(self, product_id: int):
        self.page.get_by_test_id(f"remove-{product_id}").click()
        return self

    def checkout(self):
        self.checkout_button.click()
