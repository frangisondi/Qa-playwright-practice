# QA Playwright Practice

Automated end-to-end tests for [saucedemo.com](https://www.saucedemo.com), a public demo
e-commerce site built for practicing test automation.

## What this covers

- **Login** — valid credentials, invalid credentials, empty fields
- **Cart** — adding and removing an item, verifying the cart badge count
- **Checkout** — full flow from cart through order confirmation, plus a required-field
  validation check

## Why these tests

These are the core flows a QA engineer is typically asked to validate on any e-commerce
site: can a user get in, can they add something to buy, and can they successfully pay.
Each test also checks at least one negative/edge case (bad login, missing required field)
rather than only the "happy path."

## Setup

\`\`\`bash
pip install pytest playwright
playwright install
\`\`\`

## Running the tests

\`\`\`bash
pytest test_saucedemo.py --headed
\`\`\`

Remove \`--headed\` to run without a visible browser window.

## Structure

Tests are grouped by feature area (\`TestLogin\`, \`TestAddToCart\`, \`TestCheckout\`) with a
shared \`login()\` helper to avoid repeating setup steps.
