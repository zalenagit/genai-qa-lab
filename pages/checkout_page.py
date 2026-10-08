from pages.base_page import BasePage


class CheckoutPage(BasePage):
    path = "/checkout.html"

    def fill(self, first_name: str, last_name: str, zip_code: str):
        self.page.get_by_label("First name").fill(first_name)
        self.page.get_by_label("Last name").fill(last_name)
        self.page.get_by_label("ZIP code").fill(zip_code)
        return self

    def place_order(self):
        self.page.get_by_role("button", name="Place order").click()
        return self

    @property
    def confirmation(self):
        return self.page.get_by_role("heading", name="Thank you for your order!")

    @property
    def order_id(self):
        return self.page.get_by_test_id("order-id")

    @property
    def order_total(self):
        return self.page.get_by_test_id("order-total")
