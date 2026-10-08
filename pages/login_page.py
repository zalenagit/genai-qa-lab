from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/index.html"

    def login(self, username: str, password: str):
        self.page.get_by_label("Username").fill(username)
        self.page.get_by_label("Password").fill(password)
        self.page.get_by_role("button", name="Login").click()
        return self
