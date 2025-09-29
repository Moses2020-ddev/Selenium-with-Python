# conftest.py
import os
import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pytest_html import extras

# --- Directories for screenshots and reports ---
BASE_DIR = os.path.dirname(__file__)
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# --- Generate timestamped report filename ---
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
REPORT_FILE = os.path.join(REPORTS_DIR, f"report_{timestamp}.html")

# --- Pytest CLI options ---
def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False, help="Run browser in headless mode")
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests (chrome, firefox, edge)")
    parser.addoption("--base-url", action="store", default="https://www.saucedemo.com/", help="Base URL for the application under test")

# --- Fixtures ---
@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url")

@pytest.fixture(scope="session")
def driver(request):
    browser = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1400,900")
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        service = ChromeService(ChromeDriverManager().install())
        drv = webdriver.Chrome(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    drv.implicitly_wait(5)
    yield drv
    drv.quit()

@pytest.fixture
def login_page(driver, base_url):
    return LoginPage(driver, base_url=base_url)

@pytest.fixture
def screenshot_dir():
    return SCREENSHOT_DIR

# --- Capture screenshot on any test failure ---
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        login_page_fixture = item.funcargs.get("login_page")
        username = getattr(login_page_fixture, "username", "unknown_user") if login_page_fixture else "unknown_user"
        scenario = item.name.replace("/", "_").replace(" ", "_")
        user_dir = os.path.join(SCREENSHOT_DIR, username)
        os.makedirs(user_dir, exist_ok=True)
        filename = os.path.join(user_dir, f"{scenario}.png")
        try:
            if driver:
                driver.save_screenshot(filename)
                print(f"\n[INFO] Screenshot saved to {filename}")
                # Attach screenshot to pytest-html
                if hasattr(rep, "extra"):
                    rep.extra.append(extras.image(filename, mime_type='image/png'))
                else:
                    rep.extra = [extras.image(filename, mime_type='image/png')]
        except Exception as e:
            print(f"\n[ERROR] Could not save screenshot: {e}")

# --- Consolidated test summary ---
@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    passed = failed = xfailed = blocked = 0
    for item in getattr(session, "items", []):
        rep = getattr(item, "rep_call", None)
        if rep:
            if rep.skipped and getattr(rep, "wasxfail", False):
                xfailed += 1
            elif rep.failed:
                failed += 1
            elif rep.passed:
                passed += 1
        if "blocked" in getattr(item, "keywords", {}):
            blocked += 1

    print("\n================ Test Summary ================")
    print(f"PASSED : {passed}")
    print(f"FAILED : {failed}")
    print(f"XFAILED: {xfailed}")
    print(f"BLOCKED: {blocked}")
    print("=============================================")

# --- Pytest-html integration ---
def pytest_configure(config):
    config.option.htmlpath = REPORT_FILE
    config.option.self_contained_html = True
    print(f"\n[INFO] HTML report will be saved to: {REPORT_FILE}")
