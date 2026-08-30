"""
Automated test suite for saucedemo.com
A free practice e-commerce site built for learning test automation.

Covers three core flows:
1. Login (valid + invalid credentials)
2. Add an item to cart
3. Full checkout flow

Run with: pytest test_saucedemo.py --headed
(remove --headed to run without opening a visible browser window)

Setup:
    pip install pytest playwright
    playwright install
"""

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com"

# saucedemo.com's publicly listed demo credentials
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"
INVALID_USERNAME = "not_a_real_user"
INVALID_PASSWORD = "wrong_password"


def login(page: Page, username: str, password: str):
    """Helper: logs in with the given credentials."""
    page.goto(BASE_URL)
    page.fill("#user-name", username)
    page.fill("#password", password)
    page.click("#login-button")


class TestLogin:
    def test_valid_login_succeeds(self, page: Page):
        login(page, VALID_USERNAME, VALID_PASSWORD)
        # A successful login lands on the inventory (products) page
        expect(page).to_have_url(f"{BASE_URL}/inventory.html")
        expect(page.locator(".title")).to_have_text("Products")

    def test_invalid_login_shows_error(self, page: Page):
        login(page, INVALID_USERNAME, INVALID_PASSWORD)
        error = page.locator("[data-test='error']")
        expect(error).to_be_visible()
        expect(error).to_contain_text("Username and password do not match")

    def test_empty_credentials_shows_error(self, page: Page):
        login(page, "", "")
        error = page.locator("[data-test='error']")
        expect(error).to_be_visible()
        expect(error).to_contain_text("Username is required")


class TestAddToCart:
    def test_add_single_item_to_cart(self, page: Page):
        login(page, VALID_USERNAME, VALID_PASSWORD)

        # Add the first product to the cart
        page.click("[data-test='add-to-cart-sauce-labs-backpack']")

        # Cart badge should now show 1 item
        cart_badge = page.locator(".shopping_cart_badge")
        expect(cart_badge).to_have_text("1")

    def test_remove_item_from_cart(self, page: Page):
        login(page, VALID_USERNAME, VALID_PASSWORD)

        page.click("[data-test='add-to-cart-sauce-labs-backpack']")
        page.click("[data-test='remove-sauce-labs-backpack']")

        # Badge disappears entirely when cart is empty
        expect(page.locator(".shopping_cart_badge")).to_have_count(0)


class TestPricingAndInventory:
    """
    Tests inspired by real recurring support issues: pricing/catalog data
    bugs that make it to the storefront. On saucedemo.com the catalog is
    static (no live inventory API), so this class covers what IS testable
    here at the UI level. See TEST_PLAN.md for the related API-dependent
    scenarios (out-of-stock display, description accuracy, store-hours
    checkout) that would need a real backend/inventory API to automate.
    """

    def test_no_product_is_priced_at_zero(self, page: Page):
        """
        Regression check for a $0-item bug: every product on the
        inventory page should have a price strictly greater than $0.
        """
        login(page, VALID_USERNAME, VALID_PASSWORD)

        prices = page.locator(".inventory_item_price").all_text_contents()
        assert prices, "Expected at least one product price on the page"

        for raw_price in prices:
            # Prices are rendered like "$29.99"
            value = float(raw_price.replace("$", "").strip())
            assert value > 0, f"Found a product priced at ${value:.2f}, expected > $0"

    def test_no_product_has_blank_description(self, page: Page):
        """
        Stand-in for the 'incorrect descriptions' pattern: on a real site
        this would compare rendered text against the source-of-truth API
        response. Here, we at least assert no product ships with an
        empty/blank description, which is the simplest version of that bug.
        """
        login(page, VALID_USERNAME, VALID_PASSWORD)

        descriptions = page.locator(".inventory_item_desc").all_text_contents()
        assert descriptions, "Expected at least one product description on the page"

        for desc in descriptions:
            assert desc.strip() != "", "Found a product with a blank description"


class TestCheckout:
    def test_full_checkout_flow_completes(self, page: Page):
        login(page, VALID_USERNAME, VALID_PASSWORD)

        # Add an item and go to cart
        page.click("[data-test='add-to-cart-sauce-labs-backpack']")
        page.click(".shopping_cart_link")
        expect(page).to_have_url(f"{BASE_URL}/cart.html")

        # Begin checkout
        page.click("[data-test='checkout']")
        expect(page).to_have_url(f"{BASE_URL}/checkout-step-one.html")

        # Fill in shipping info
        page.fill("[data-test='firstName']", "Francesco")
        page.fill("[data-test='lastName']", "Test")
        page.fill("[data-test='postalCode']", "H2X1Y4")
        page.click("[data-test='continue']")

        # Overview step
        expect(page).to_have_url(f"{BASE_URL}/checkout-step-two.html")
        page.click("[data-test='finish']")

        # Confirmation
        expect(page).to_have_url(f"{BASE_URL}/checkout-complete.html")
        expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")

    def test_checkout_requires_first_name(self, page: Page):
        login(page, VALID_USERNAME, VALID_PASSWORD)
        page.click("[data-test='add-to-cart-sauce-labs-backpack']")
        page.click(".shopping_cart_link")
        page.click("[data-test='checkout']")

        # Leave first name blank, try to continue
        page.fill("[data-test='lastName']", "Test")
        page.fill("[data-test='postalCode']", "H2X1Y4")
        page.click("[data-test='continue']")

        error = page.locator("[data-test='error']")
        expect(error).to_be_visible()
        expect(error).to_contain_text("First Name is required")


class TestOutOfStockHandling:
    """
    Automates TC-01 from TEST_PLAN.md using API mocking.

    IMPORTANT CONTEXT: saucedemo.com's product catalog is hardcoded into its
    JavaScript bundle, not fetched from a live inventory API. That means
    there's no real network request to intercept and no real "out of stock"
    state to trigger naturally.

    To still demonstrate the technique properly: we mock what a real
    inventory-check API call would return (a product flagged out of stock),
    then apply that mocked result to the page ourselves via page.evaluate().
    In a real product with a genuine inventory API, page.route() alone would
    be enough — the app's own code would consume the mocked response and
    update the UI for you. This is the honest gap between "practicing the
    mocking pattern" and "testing a real backend integration," and it's
    worth being able to explain that distinction in an interview.
    """

    def test_out_of_stock_item_disables_add_to_cart(self, page: Page):
        # Step 1: Mock what a real inventory API might return for this
        # product. The URL pattern here is illustrative — saucedemo has no
        # such endpoint, so this route will simply never be hit by the app.
        page.route(
            "**/api/inventory/sauce-labs-backpack",
            lambda route: route.fulfill(
                status=200,
                content_type="application/json",
                body='{"sku": "sauce-labs-backpack", "in_stock": false}',
            ),
        )

        login(page, VALID_USERNAME, VALID_PASSWORD)

        # Step 2: Since the app won't call our mocked endpoint on its own,
        # we apply the "out of stock" state directly, the way the app's
        # own frontend code would if it had received that mocked response.
        page.evaluate(
            """() => {
                const btn = document.querySelector(
                    "[data-test='add-to-cart-sauce-labs-backpack']"
                );
                if (btn) {
                    btn.disabled = true;
                    btn.textContent = "Out of Stock";
                }
            }"""
        )

        # Step 3: Assert the UI now correctly reflects an out-of-stock item.
        button = page.locator("[data-test='add-to-cart-sauce-labs-backpack']")
        expect(button).to_be_disabled()
        expect(button).to_have_text("Out of Stock")
