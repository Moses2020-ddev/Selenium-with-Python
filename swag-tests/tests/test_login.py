# tests/test_login.py
import os
import time
import pytest
from PIL import Image, ImageChops
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERS = {
    "standard_user": "secret_sauce",
    "locked_out_user": "secret_sauce",
    "problem_user": "secret_sauce",
    "performance_glitch_user": "secret_sauce",
    "error_user": "secret_sauce",
    "visual_user": "secret_sauce",
}

INVALID_USERS = {
    "wrong_user": "secret_sauce"
}

# ---------- Visual regression helper ----------
def compare_images(baseline_path, current_path, diff_path):
    im1 = Image.open(baseline_path).convert("RGBA")
    im2 = Image.open(current_path).convert("RGBA")

    if im1.size != im2.size:
        im2 = im2.resize(im1.size)

    diff = ImageChops.difference(im1, im2)
    if diff.getbbox() is None:
        return True

    diff.save(diff_path)
    return False

# ---------- LOGIN TESTS ----------
@pytest.mark.parametrize("username,password", [(u, p) for u, p in USERS.items()])
def test_valid_login(login_page, username, password, screenshot_dir):
    timeout = 40 if username in ["performance_glitch_user", "problem_user", "error_user"] else 15

    login_page.load()
    start = time.time()
    login_page.login(username, password)

    # Locked out user should show error
    if username == "locked_out_user":
        err = login_page.get_error_text(timeout=10)
        assert err and "locked" in err.lower()
        return

    # Error user may show error or succeed
    if username == "error_user":
        err = login_page.get_error_text(timeout=10)
        if err:
            assert "error" in err.lower() or "not allowed" in err.lower()
        else:
            assert login_page.wait_for_inventory(timeout=timeout)
        return

    # Other users should reach inventory page
    assert login_page.wait_for_inventory(timeout=timeout), f"{username} failed to load inventory page"

    # Performance check
    elapsed = time.time() - start
    if username == "performance_glitch_user":
        assert elapsed < 35, f"Login took too long: {elapsed:.1f}s"

    # Visual regression check
    if username == "visual_user":
        baseline_path = os.path.join(screenshot_dir, "visual_user_baseline.png")
        current_path = os.path.join(screenshot_dir, "visual_user_current.png")
        diff_path = os.path.join(screenshot_dir, "visual_user_diff.png")

        os.makedirs(screenshot_dir, exist_ok=True)
        login_page.driver.save_screenshot(current_path)

        if not os.path.exists(baseline_path):
            os.rename(current_path, baseline_path)
            pytest.xfail("Baseline image created for visual_user. Re-run to compare.")

        identical = compare_images(baseline_path, current_path, diff_path)
        assert identical, f"Visual diff detected for visual_user. See {diff_path}"

# ---------- INVALID LOGIN TESTS ----------
@pytest.mark.parametrize("username,password", [(u, p) for u, p in INVALID_USERS.items()])
def test_invalid_login(login_page, username, password, screenshot_dir):
    login_page.load()
    login_page.login(username, password)

    err = WebDriverWait(login_page.driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    ).text
    assert err, f"Expected error message for invalid login: {username}"

# ---------- MENU VERIFICATION TEST ----------
@pytest.mark.parametrize("username,password", [(u, p) for u, p in USERS.items()])
def test_menu_and_logout(login_page, username, password):
    if username == "locked_out_user":
        pytest.skip(f"{username} cannot log in; skipping menu test")

    login_page.load()
    login_page.login(username, password)
    login_page.wait_for_inventory(timeout=15)

    # Verify menu button
    assert login_page.is_menu_present(), f"Menu button not visible for {username}"

    # Open menu and check logout link
    login_page.driver.find_element(*login_page.menu_button).click()
    logout = WebDriverWait(login_page.driver, 10).until(
        EC.visibility_of_element_located(login_page.logout_link)
    )
    assert logout.is_displayed(), f"Logout link not visible in menu for {username}"

    # Logout
    logout.click()
    assert login_page.is_login_button_present(), f"{username} failed to logout"

# ---------- CART TESTS ----------
@pytest.mark.parametrize("username,password", [(u, p) for u, p in USERS.items()])
def test_add_remove_products(login_page, username, password):
    if username in ["locked_out_user", "error_user"]:
        pytest.skip(f"{username} cannot perform cart operations")

    login_page.load()
    login_page.login(username, password)
    login_page.wait_for_inventory(timeout=15)

    # Add first 2 products to cart
    add_buttons = login_page.driver.find_elements(By.CSS_SELECTOR, ".inventory_item button")
    for btn in add_buttons[:2]:
        btn.click()

    # Go to cart
    login_page.driver.find_element(By.CSS_SELECTOR, ".shopping_cart_link").click()
    cart_items = WebDriverWait(login_page.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart_item"))
    )
    assert len(cart_items) == 2, f"{username} cart should have 2 items"

    # Remove items
    remove_buttons = login_page.driver.find_elements(By.CSS_SELECTOR, ".cart_item button")
    for btn in remove_buttons:
        btn.click()

    WebDriverWait(login_page.driver, 10).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, ".cart_item")) == 0
    )
    cart_items = login_page.driver.find_elements(By.CSS_SELECTOR, ".cart_item")
    assert len(cart_items) == 0, f"{username} cart not empty after removing"

# ---------- CHECKOUT FLOW ----------
@pytest.mark.parametrize("username,password", [(u, p) for u, p in USERS.items()])
def test_checkout_flow(login_page, username, password):
    if username in ["locked_out_user", "error_user"]:
        pytest.skip(f"{username} cannot perform checkout")

    login_page.load()
    login_page.login(username, password)
    login_page.wait_for_inventory(timeout=15)

    # Add first product to cart
    login_page.driver.find_element(By.CSS_SELECTOR, ".inventory_item button").click()

    # Go to cart
    login_page.driver.find_element(By.CSS_SELECTOR, ".shopping_cart_link").click()
    WebDriverWait(login_page.driver, 10).until(
        EC.presence_of_element_located((By.ID, "cart_contents_container"))
    )

    # Checkout
    login_page.driver.find_element(By.ID, "checkout").click()
    WebDriverWait(login_page.driver, 10).until(
        EC.presence_of_element_located((By.ID, "checkout_info_container"))
    )

    # Fill checkout info
    login_page.driver.find_element(By.ID, "first-name").send_keys("Test")
    login_page.driver.find_element(By.ID, "last-name").send_keys("User")
    login_page.driver.find_element(By.ID, "postal-code").send_keys("00100")
    login_page.driver.find_element(By.ID, "continue").click()

    WebDriverWait(login_page.driver, 10).until(
        EC.presence_of_element_located((By.ID, "checkout_summary_container"))
    )

    # Finish checkout
    login_page.driver.find_element(By.ID, "finish").click()
    WebDriverWait(login_page.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
    )

    complete_text = login_page.driver.find_element(By.CLASS_NAME, "complete-header").text
    assert "THANK YOU" in complete_text.upper(), f"{username} checkout did not complete"

    # Logout after checkout
    login_page.logout()
    assert login_page.is_login_button_present(), f"{username} failed to logout after checkout"
