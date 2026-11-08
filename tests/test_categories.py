
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from config.config import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    EVENT_URL
)


def test_category_list_page(driver):

    assert ADMIN_EMAIL, "Email is missing"
    assert ADMIN_PASSWORD, "Password is missing"

    # Step 1: Login
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)

    # Wait until the dashboard is displayed
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element(
        (By.TAG_NAME, "body"),
        "Your upcoming events"
        )
    )

    print("\nLOGIN SUCCESSFUL")
    print("Login URL:", driver.current_url)

    # Step 2: Open event dashboard
    driver.get(EVENT_URL)

    print("\nEVENT URL:", EVENT_URL)
    print("ACTUAL EVENT URL:", driver.current_url)
    print("EVENT PAGE TITLE:", driver.title)

    event_body = driver.find_element("tag name", "body").text
    print("\nEVENT PAGE CONTENT:")
    print(event_body[:2000])

    # Step 3: Open category page
    category_url = f"{EVENT_URL}categories/"
    driver.get(category_url)

    print("\nCATEGORY URL:", category_url)
    print("ACTUAL CATEGORY URL:", driver.current_url)
    print("CATEGORY PAGE TITLE:", driver.title)

    category_body = driver.find_element("tag name", "body").text
    print("\nCATEGORY PAGE CONTENT:")
    print(category_body[:3000])

    driver.save_screenshot("screenshots/category_debug.png")
    # Verify category page
    assert "/categories/" in driver.current_url
    assert "Product categories" in category_body
    assert "Create a new category" in category_body
