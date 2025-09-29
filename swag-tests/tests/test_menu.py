import pytest

@pytest.mark.parametrize("username,password", [("standard_user", "secret_sauce")])
def test_menu_and_logout(login_page, username, password, screenshot_dir):
    login_page.load()
    login_page.login(username, password)
    assert login_page.wait_for_inventory(), "Inventory page not loaded"

    # Check menu button
    assert login_page.is_menu_present(), "Menu button not visible"

    # Open menu and check logout link
    login_page.logout()
    assert login_page.is_login_button_present(), "Logout failed"
