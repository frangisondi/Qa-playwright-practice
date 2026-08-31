from playwright.sync_api import Page

BASE_URL = "https://www.saucedemo.com"


class LoginPage:
    """Represents the saucedemo login page: its elements and actions."""

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")

    def goto(self):
        self.page.goto(BASE_URL)

    def login(self, username: str, password: str):
        """Full login flow: navigate, fill fields, submit."""
        self.goto()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
