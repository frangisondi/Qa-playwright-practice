from playwright.sync_api import Page

BASE_URL = "https://www.saucedemo.com"


class CartPage:
    """Represents the cart page."""

    URL = f"{BASE_URL}/cart.html"

    def __init__(self, page: Page):
        self.page = page
        self.checkout_button = page.locator("[data-test='checkout']")

    def checkout(self):
        self.checkout_button.click()
