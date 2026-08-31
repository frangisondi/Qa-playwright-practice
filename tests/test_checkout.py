import pytest
from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
    CheckoutCompletePage,
)


class TestCheckout:
    def test_full_checkout_flow_completes(self, logged_in_page: Page):
        page = logged_in_page
        inventory_page = InventoryPage(page)
        inventory_page.add_to_cart("sauce-labs-backpack")
        inventory_page.go_to_cart()
        expect(page).to_have_url(CartPage.URL)

        cart_page = CartPage(page)
        cart_page.checkout()
        expect(page).to_have_url(CheckoutStepOnePage.URL)

        step_one = CheckoutStepOnePage(page)
        step_one.fill_info(
            first_name="Francesco", last_name="Test", postal_code="H2X1Y4"
        )
        step_one.continue_to_overview()
        expect(page).to_have_url(CheckoutStepTwoPage.URL)

        step_two = CheckoutStepTwoPage(page)
        step_two.finish()
        expect(page).to_have_url(CheckoutCompletePage.URL)

        complete_page = CheckoutCompletePage(page)
        expect(complete_page.complete_header).to_have_text("Thank you for your order!")

    @pytest.mark.parametrize(
        "field_to_leave_blank, expected_error",
        [
            ("first_name", "First Name is required"),
            ("last_name", "Last Name is required"),
            ("postal_code", "Postal Code is required"),
        ],
    )
    def test_checkout_requires_each_field(
        self, logged_in_page: Page, field_to_leave_blank: str, expected_error: str
    ):
        """Runs once per required field, confirming its specific error message."""
        page = logged_in_page
        all_fields = {
            "first_name": "Francesco",
            "last_name": "Test",
            "postal_code": "H2X1Y4",
        }
        fields_to_fill = {
            key: value
            for key, value in all_fields.items()
            if key != field_to_leave_blank
        }

        inventory_page = InventoryPage(page)
        inventory_page.add_to_cart("sauce-labs-backpack")
        inventory_page.go_to_cart()

        cart_page = CartPage(page)
        cart_page.checkout()

        step_one = CheckoutStepOnePage(page)
        step_one.fill_info(**fields_to_fill)
        step_one.continue_to_overview()

        expect(step_one.error_message).to_be_visible()
        expect(step_one.error_message).to_contain_text(expected_error)
