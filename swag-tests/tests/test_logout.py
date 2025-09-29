import pytest

@pytest.mark.parametrize("username,password", [("standard_user","secret_sauce")])
def test_logout(login_page, username, password):
    login_page.load()
    login_page.login(username, password)
    assert login_page.wait_for_inventory()

    login_page.logout()
    assert login_page.is_login_button_present(), "Logout failed"
