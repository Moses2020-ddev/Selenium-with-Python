import pytest
from pages.inventory_page import InventoryPage

PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]

@pytest.mark.parametrize("username,password", [("standard_user", "secret_sauce")])
def test_add_remove_products(login_page, username, password):
    login_page.load()
    login_page.login(username, password)
    assert login_page.wait_for_inventory()

    inventory = InventoryPage(login_page.driver)

    # Add products to cart
    for product in PRODUCTS:
        inventory.add_product_to_cart(product)

    assert inventory.get_cart_count() == len(PRODUCTS), "Cart count mismatch after adding"

    # Remove products from cart
    for product in PRODUCTS:
        inventory.remove_product_from_cart(product)

    assert inventory.get_cart_count() == 0, "Cart not empty after removing"
