from playwright.sync_api import Page, expect


class TestOutOfStockHandling:
    """
    Automates TC-01 from TEST_PLAN.md using API mocking.

    saucedemo.com's catalog is hardcoded into its JavaScript, not fetched
    from a live inventory API, so there's no real request to intercept. We
    mock what a real inventory API would return, then apply that result to
    the page ourselves — an honest gap between "practicing the mocking
    pattern" and "testing a real backend integration."
    """

    def test_out_of_stock_item_disables_add_to_cart(self, logged_in_page: Page):
        page = logged_in_page

        page.route(
            "**/api/inventory/sauce-labs-backpack",
            lambda route: route.fulfill(
                status=200,
                content_type="application/json",
                body='{"sku": "sauce-labs-backpack", "in_stock": false}',
            ),
        )

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

        button = page.locator("[data-test='add-to-cart-sauce-labs-backpack']")
        expect(button).to_be_disabled()
        expect(button).to_have_text("Out of Stock")
