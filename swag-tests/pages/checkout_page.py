from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

    # Locators
    first_name = (By.ID, "first-name")
    last_name = (By.ID, "last-name")
    postal_code = (By.ID, "postal-code")
    continue_btn = (By.ID, "continue")
    finish_btn = (By.ID, "finish")
    complete_header = (By.CLASS_NAME, "complete-header")
    error_msg = (By.CSS_SELECTOR, "h3[data-test='error']")

    def fill_info(self, first, last, postal):
        self.driver.find_element(*self.first_name).clear()
        self.driver.find_element(*self.first_name).send_keys(first)
        self.driver.find_element(*self.last_name).clear()
        self.driver.find_element(*self.last_name).send_keys(last)
        self.driver.find_element(*self.postal_code).clear()
        self.driver.find_element(*self.postal_code).send_keys(postal)

    def continue_checkout(self):
        self.driver.find_element(*self.continue_btn).click()

    def finish_checkout(self):
        self.driver.find_element(*self.finish_btn).click()

    def is_complete(self):
        try:
            el = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.complete_header)
            )
            return el.is_displayed()
        except:
            return False

    def has_error(self):
        try:
            el = self.driver.find_element(*self.error_msg)
            return el.is_displayed()
        except:
            return False
