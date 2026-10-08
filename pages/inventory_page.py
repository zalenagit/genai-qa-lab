from pages.base_page import BasePage


class InventoryPage(BasePage):
    path = "/inventory.html"

    @property
    def heading(self):
        return self.page.get_by_role("heading", name="Products")

    @property
    def products(self):
        return self.page.locator("[data-testid^=product-]")

    def add_to_cart(self, product_id: int, times: int = 1):
        for _ in range(times):
            self.page.get_by_test_id(f"add-{product_id}").click()
        return self

    def go_to_cart(self):
        self.page.get_by_role("link", name="Cart").click()
