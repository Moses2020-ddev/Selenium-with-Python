from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, driver, base_url=None):
        self.driver = driver
        if base_url:
            self.URL = base_url

    # --- Locators ---
    username_input = (By.ID, "user-name")
    password_input = (By.ID, "password")
    login_button = (By.ID, "login-button")
    error_container = (By.CSS_SELECTOR, "h3[data-test='error']")
    inventory_container = (By.ID, "inventory_container")
    products_title = (By.CLASS_NAME, "title")
    menu_button = (By.ID, "react-burger-menu-btn")
    logout_link = (By.ID, "logout_sidebar_link")

    # --- Page Actions ---
    def load(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.driver.find_element(*self.username_input).clear()
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).clear()
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def wait_for_inventory(self, timeout=10):
        """Wait until inventory page is loaded"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.inventory_container)
        )

    def get_error_text(self, timeout=5):
        """Return error message if visible"""
        try:
            el = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.error_container)
            )
            return el.text.strip()
        except:
            return None

    def is_menu_present(self):
        """Check if the menu button is visible"""
        try:
            return self.driver.find_element(*self.menu_button).is_displayed()
        except:
            return False

    def logout(self, timeout=5):
        """Logout from the app"""
        if self.is_menu_present():
            self.driver.find_element(*self.menu_button).click()
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.logout_link)
            ).click()
            # wait until login button is visible again
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.login_button)
            )

    def is_login_button_present(self):
        """Check if login button is visible (after logout)"""
        try:
            return self.driver.find_element(*self.login_button).is_displayed()
        except:
            return False
