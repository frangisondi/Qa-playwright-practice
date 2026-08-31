import pytest
from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage, ALL_PRODUCTS


class TestAddToCart:
    @pytest.mark.parametrize("product_slug", ALL_PRODUCTS)
    def test_add_single_item_to_cart(self, logged_in_page: Page, product_slug: str):
        """Runs once per product — confirms every product can be added."""
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.add_to_cart(product_slug)

        expect(inventory_page.cart_badge).to_have_text("1")

    @pytest.mark.parametrize("product_slug", ALL_PRODUCTS)
    def test_remove_item_from_cart(self, logged_in_page: Page, product_slug: str):
        """Runs once per product — confirms every product can be removed."""
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.add_to_cart(product_slug)
        inventory_page.remove_from_cart(product_slug)

        expect(inventory_page.cart_badge).to_have_count(0)
