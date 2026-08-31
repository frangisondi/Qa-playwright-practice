# QA Playwright Practice

Automated end-to-end tests for saucedemo.com, structured as a real Page
Object Model (POM) framework — not just a single test file.

## Project structure

```
qa-playwright-practice/
├── pages/              # Page Object classes (one per page of the site)
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── conftest.py     # shared fixtures (e.g. logged_in_page)
│   ├── test_login.py
│   ├── test_cart.py
│   ├── test_pricing_inventory.py
│   ├── test_checkout.py
│   └── test_out_of_stock.py
├── .github/workflows/tests.yml   # CI: runs tests on every push
├── pytest.ini           # HTML reports + auto-retry for flaky tests
├── requirements.txt
└── TEST_PLAN.md          # documented test cases that need a real API
```

## Why Page Object Model

Instead of every test file containing its own copy of CSS selectors, each
page of the site gets one class (in `pages/`) that owns its selectors and
actions. Tests then read like plain English — `inventory_page.add_to_cart(...)`
instead of `page.click("[data-test='add-to-cart-...']")` repeated everywhere.
If the site's HTML changes, you fix the selector in one place.

## Setup

```bash
pip install -r requirements.txt
playwright install
```

## Running the tests

```bash
pytest --headed
```

This also generates `report.html` — open it in a browser for a readable,
clickable test report instead of scrolling terminal output.

### Cross-browser

```bash
pytest --browser chromium --browser firefox --browser webkit
```

Runs the whole suite once per browser.

### CI

Every push to `main` automatically runs the full suite via GitHub Actions
(see `.github/workflows/tests.yml`), and uploads the HTML report as a
downloadable artifact on the run's summary page.

## Notes

- `test_cart.py` and part of `test_checkout.py` use `pytest.mark.parametrize`
  to run the same test logic across multiple inputs (every product, every
  required checkout field) instead of writing near-duplicate tests.
- `test_out_of_stock.py` demonstrates API mocking with `page.route()` —
  see the docstring in that file for an honest note on its limitation
  against this particular site.
- A failing test isn't always a bad thing — see `TEST_PLAN.md` and the
  Aliments-Morales client repo for a real example of a test correctly
  catching a genuine bug.
