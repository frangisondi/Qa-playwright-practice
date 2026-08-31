"""
Shared fixtures for the whole test suite. pytest auto-discovers this file
and makes any fixture defined here available in every test, without needing
to import it.
"""

import pytest
from playwright.sync_api import Page

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"
INVALID_USERNAME = "not_a_real_user"
INVALID_PASSWORD = "wrong_password"


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """
    A page that's already logged in as the standard user. Any test that
    just needs "I'm logged in, now let's test X" can use this fixture
    instead of repeating login(page, VALID_USERNAME, VALID_PASSWORD) in
    every single test.

    Usage: def test_something(self, logged_in_page):
    """
    login_page = LoginPage(page)
    login_page.login(VALID_USERNAME, VALID_PASSWORD)
    return page


@pytest.fixture
def inventory_page(logged_in_page: Page) -> InventoryPage:
    """
    A ready-to-use InventoryPage object, already logged in. Notice this
    fixture depends on another fixture (logged_in_page) — pytest resolves
    that automatically.
    """
    return InventoryPage(logged_in_page)
