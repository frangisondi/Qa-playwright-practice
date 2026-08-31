from playwright.sync_api import Page

BASE_URL = "https://www.saucedemo.com"


class CheckoutStepOnePage:
    """Shipping info form (step 1 of checkout)."""

    URL = f"{BASE_URL}/checkout-step-one.html"

    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.error_message = page.locator("[data-test='error']")

    def fill_info(self, first_name: str = None, last_name: str = None, postal_code: str = None):
        """
        Fills whichever fields are given. Pass None (or just omit) for a
        field to deliberately leave it blank — used by validation tests.
        """
        if first_name is not None:
            self.first_name_input.fill(first_name)
        if last_name is not None:
            self.last_name_input.fill(last_name)
        if postal_code is not None:
            self.postal_code_input.fill(postal_code)

    def continue_to_overview(self):
        self.continue_button.click()


class CheckoutStepTwoPage:
    """Order overview page (step 2 of checkout)."""

    URL = f"{BASE_URL}/checkout-step-two.html"

    def __init__(self, page: Page):
        self.page = page
        self.finish_button = page.locator("[data-test='finish']")

    def finish(self):
        self.finish_button.click()


class CheckoutCompletePage:
    """Order confirmation page (final step)."""

    URL = f"{BASE_URL}/checkout-complete.html"

    def __init__(self, page: Page):
        self.page = page
        self.complete_header = page.locator(".complete-header")
