# Swag Labs Automated Tests

This repository contains automated UI tests for [Swag Labs](https://www.saucedemo.com/) using **Selenium**, **pytest**, and the **Page Object Model (POM)** design pattern.  

The goal is to validate core user journeys such as login, navigation, cart management, checkout, and logout.

---

## ✅ Features Tested

- **Login**
  - Standard user login
  - Invalid login with wrong credentials
  - Locked out user scenario (expected error message)
  - Logout after login

- **Menu**
  - Open side menu
  - Verify menu items
  - Logout through menu

- **Cart**
  - Add products to cart
  - Remove products from cart
  - Validate cart count

- **Checkout**
  - Checkout flow with valid details
  - Verify order completion

---

## 🧪 Planned / Upcoming Tests

- Problem user (unexpected behaviors)
- Performance glitch user (slow page loads)
- Error user
- Visual user (UI differences)
- Extended negative login scenarios

---

## 🛠️ Tech Stack

- **Python 3**
- **pytest** (test runner)
- **Selenium WebDriver**
- **Pillow** (visual regression checks)
- **pytest-html** (HTML reporting)
- **pytest-xdist** (parallel test execution)

---

## ▶️ Running the Tests

1. Clone the repo  
 
   git clone https://github.com/Moses2020-ddev/swag-tests.git
   cd swag-tests
Install dependencies


pip install -r requirements.txt
Run tests


pytest --html=reports/report.html --self-contained-html
To run tests in parallel


pytest -n auto --html=reports/report.html --self-contained-html
📋 Test Cases Overview
Test Case	Scenario	Expected Result
TC01	Login with standard_user	Redirect to inventory page
TC02	Login with wrong credentials	Error message displayed
TC03	Login with locked_out_user	Locked out error displayed
TC04	Menu navigation	Menu opens, options visible
TC05	Add product to cart	Cart updates with product
TC06	Remove product from cart	Cart is empty
TC07	Checkout with valid details	Order completed successfully
TC08	Logout	Redirect back to login page
TC09	Login with problem_user	Handles unexpected behavior (planned)
TC10	Login with performance_glitch_user	Handles delayed load (planned)
TC11	Login with error_user	Shows error or loads inventory (planned)
TC12	Login with visual_user	UI matches baseline (planned)

📂 Project Structure

swag-tests/
├─ pages/              # Page Object Models
│  ├─ login_page.py
│  ├─ inventory_page.py
│  ├─ cart_page.py
│  ├─ checkout_page.py
│  └─ menu_page.py
├─ tests/              # Test cases
│  ├─ test_login.py
│  ├─ test_menu.py
│  ├─ test_cart.py
│  ├─ test_checkout.py
│  └─ test_logout.py
├─ conftest.py         # Pytest fixtures & setup
├─ requirements.txt    # Dependencies
└─ reports/            # Test reports (HTML)

📊 Reporting
Tests generate HTML reports under the reports/ folder.
Includes details of passed, failed, and skipped scenarios.
Visual diffs are stored if UI mismatches occur (visual_user).

🙌 Contribution
Pull requests and improvements are welcome. Planned next steps include:
Expanding negative test coverage
Improving visual regression baselines
CI integration with GitHub Actions


