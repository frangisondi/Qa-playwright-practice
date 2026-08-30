# Test Plan: Inventory & Catalog Integrity

These test cases are based on real recurring issues seen in production support:
catalog and inventory data problems that surface on the storefront. They are
documented here as designed test cases rather than automated, because they
depend on a live backend/inventory API that a static demo site
(saucedemo.com) doesn't have. Two related, fully automated tests
(`test_no_product_is_priced_at_zero`, `test_no_product_has_blank_description`)
live in `test_saucedemo.py`.

Documenting untestable-in-this-environment cases like this is itself a normal
part of QA work — you plan the full test coverage a feature needs, then flag
which cases require API/backend access, test data, or environment changes
before they can be automated.

---

## TC-01: Out-of-stock item still shows "Add to Cart" — ✅ Automated

> Implemented in `test_saucedemo.py` as `TestOutOfStockHandling::test_out_of_stock_item_disables_add_to_cart`,
> using API-response mocking combined with direct DOM state injection (since
> saucedemo has no real inventory API for the mock to naturally connect to).
> See the docstring on that test class for the full explanation of that
> workaround.


**Issue pattern:** Items marked out-of-stock in inventory still appear
available for purchase on the storefront.

**Preconditions:** A product in the inventory API is flagged `in_stock: false`.

**Steps:**
1. Load the product listing page.
2. Locate the out-of-stock product.

**Expected result:** The "Add to Cart" button is disabled or replaced with an
"Out of Stock" label. The item cannot be added to the cart.

**Why it needs an API:** saucedemo's product list is static HTML with no
stock-status field to manipulate, so this state can't be triggered here.

---

## TC-02: Product description doesn't match catalog/API data

**Issue pattern:** The description rendered on the page doesn't match what's
stored as the source of truth (stale cache, mistranslation, wrong SKU mapped).

**Preconditions:** Known-good description text for a product is available
from the inventory API.

**Steps:**
1. Fetch the product's description via the API.
2. Load the same product on the storefront.
3. Compare the two strings.

**Expected result:** Rendered description exactly matches the API's value.

**Why it needs an API:** There's no independent source of truth to compare
against on a static demo site — `test_no_product_has_blank_description` in
the test suite covers the simplest version of this (catching empty output).

---

## TC-03: Checkout allowed after posted store hours

**Issue pattern:** A customer can complete checkout even though the store's
listed hours say it's closed.

**Preconditions:** Store hours are configurable/mockable in a test
environment (e.g. hours set to "closed" for the current time).

**Steps:**
1. Set store status to closed (via API or admin/test config).
2. Add an item to cart and proceed to checkout.
3. Attempt to complete the order.

**Expected result:** Checkout is blocked with a clear message (e.g. "Store is
currently closed — orders can be placed after 9:00 AM"), and no order is
created.

**Why it needs an API:** Store hours and "current time" need to be
controllable in the test, which requires backend/config access saucedemo
doesn't expose.
