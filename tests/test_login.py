import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from config.config import ADMIN_EMAIL, ADMIN_PASSWORD


def test_user_login(driver):

    assert ADMIN_EMAIL, "Email is missing"
    assert ADMIN_PASSWORD, "Password is missing"

    login_page = LoginPage(driver)

    # Step 1: Open login page
    login_page.open_login_page()

    # Step 2: Enter credentials and login
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)

    # Step 3: Wait for dashboard URL
    WebDriverWait(driver, 20).until(
        EC.url_to_be("http://127.0.0.1:8000/control/")
    )

    # Step 4: Wait for dashboard content
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            "Your upcoming events"
        )
    )

    # Step 5: Verify login
    body_text = driver.find_element(
        By.TAG_NAME, "body"
    ).text

    print("\nCurrent URL:", driver.current_url)
    print("\nPAGE CONTENT AFTER LOGIN:\n")
    print(body_text)

    assert "Dashboard" in body_text
    assert "Your upcoming events" in body_text

    # Step 6: Screenshot
    os.makedirs("screenshots", exist_ok=True)

    driver.save_screenshot(
        "screenshots/login_result.png"
    )
