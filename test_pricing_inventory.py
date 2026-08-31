from playwright.sync_api import Page

from pages.inventory_page import InventoryPage


class TestPricingAndInventory:
    """
    Tests inspired by real recurring support issues: pricing/catalog data
    bugs that make it to the storefront. See TEST_PLAN.md for related
    API-dependent scenarios that need a real backend to automate.
    """

    def test_no_product_is_priced_at_zero(self, logged_in_page: Page):
        inventory_page = InventoryPage(logged_in_page)
        prices = inventory_page.get_all_prices()

        assert prices, "Expected at least one product price on the page"
        for value in prices:
            assert value > 0, f"Found a product priced at ${value:.2f}, expected > $0"

    def test_no_product_has_blank_description(self, logged_in_page: Page):
        inventory_page = InventoryPage(logged_in_page)
        descriptions = inventory_page.get_all_descriptions()

        assert descriptions, "Expected at least one product description on the page"
        for desc in descriptions:
            assert desc.strip() != "", "Found a product with a blank description"
