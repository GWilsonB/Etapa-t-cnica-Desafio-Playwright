from playwright.sync_api import Page


class LoginPage:
    URL = "/login"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.heading = page.get_by_role("heading", name="Login")
        self.error_alert = page.get_by_role("alert")

    def open(self) -> None:
        self.page.goto(self.URL)

    def login(self, email: str, password: str) -> None:
        self.page.get_by_test_id("email").fill(email)
        self.page.get_by_test_id("senha").fill(password)
        self.page.get_by_test_id("entrar").click()
