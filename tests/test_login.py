from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from .conftest import VALID_USERNAME, VALID_PASSWORD, INVALID_USERNAME, INVALID_PASSWORD


class TestLogin:
    def test_valid_login_succeeds(self, page: Page):
        login_page = LoginPage(page)
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        inventory_page = InventoryPage(page)
        expect(page).to_have_url(InventoryPage.URL)
        expect(inventory_page.title).to_have_text("Products")

    def test_invalid_login_shows_error(self, page: Page):
        login_page = LoginPage(page)
        login_page.login(INVALID_USERNAME, INVALID_PASSWORD)

        expect(login_page.error_message).to_be_visible()
        expect(login_page.error_message).to_contain_text(
            "Username and password do not match"
        )

    def test_empty_credentials_shows_error(self, page: Page):
        login_page = LoginPage(page)
        login_page.login("", "")

        expect(login_page.error_message).to_be_visible()
        expect(login_page.error_message).to_contain_text("Username is required")
