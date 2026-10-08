from playwright.sync_api import Page


class BasePage:
    """Shared behavior for every page object."""

    path = "/"

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def open(self):
        self.page.goto(self.base_url + self.path)
        return self

    @property
    def cart_count(self):
        return self.page.get_by_test_id("cart-count")

    @property
    def error(self):
        return self.page.get_by_role("alert")
