import pytest
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage

@pytest.mark.parametrize("username,password", [("standard_user", "secret_sauce")])
def test_checkout_flow(login_page, username, password):
    login_page.load()
    login_page.login(username, password)
    assert login_page.wait_for_inventory()

    inventory = InventoryPage(login_page.driver)
    inventory.add_product_to_cart("Sauce Labs Backpack")
    inventory.go_to_cart()

    checkout = CheckoutPage(login_page.driver)

    # Negative: missing info
    checkout.continue_checkout()
    assert checkout.has_error(), "Expected error for missing checkout info"

    # Positive: fill info and complete checkout
    checkout.fill_info("John", "Doe", "12345")
    checkout.continue_checkout()
    checkout.finish_checkout()
    assert checkout.is_complete(), "Checkout not completed successfully"
