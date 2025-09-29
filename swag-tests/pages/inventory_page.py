from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver

    # Locators
    cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
    cart_link = (By.CLASS_NAME, "shopping_cart_link")

    def add_product_to_cart(self, product_name):
        """Add a product to cart by its name"""
        btn = self.driver.find_element(By.XPATH, f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button")
        btn.click()

    def remove_product_from_cart(self, product_name):
        """Remove a product from cart by its name"""
        btn = self.driver.find_element(By.XPATH, f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button[contains(text(),'Remove')]")
        btn.click()

    def get_cart_count(self):
        """Return number of items in cart"""
        try:
            count_el = self.driver.find_element(*self.cart_badge)
            return int(count_el.text)
        except:
            return 0

    def go_to_cart(self):
        self.driver.find_element(*self.cart_link).click()
        # wait for cart page to load
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
        )
