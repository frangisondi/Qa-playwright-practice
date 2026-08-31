from playwright.sync_api import Page

BASE_URL = "https://www.saucedemo.com"

# All 6 products on the site, by the slug used in their data-test attributes
ALL_PRODUCTS = [
    "sauce-labs-backpack",
    "sauce-labs-bike-light",
    "sauce-labs-bolt-t-shirt",
    "sauce-labs-fleece-jacket",
    "sauce-labs-onesie",
    "test.allthethings()-t-shirt-(red)",
]


class InventoryPage:
    """Represents the product listing page (after login)."""

    URL = f"{BASE_URL}/inventory.html"

    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator(".title")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.prices = page.locator(".inventory_item_price")
        self.descriptions = page.locator(".inventory_item_desc")

    def add_to_cart(self, product_slug: str):
        self.page.click(f"[data-test='add-to-cart-{product_slug}']")

    def remove_from_cart(self, product_slug: str):
        self.page.click(f"[data-test='remove-{product_slug}']")

    def go_to_cart(self):
        self.cart_link.click()

    def get_all_prices(self) -> list[float]:
        """Returns every listed price as a float, e.g. [29.99, 9.99, ...]."""
        raw_prices = self.prices.all_text_contents()
        return [float(p.replace("$", "").strip()) for p in raw_prices]

    def get_all_descriptions(self) -> list[str]:
        return self.descriptions.all_text_contents()
