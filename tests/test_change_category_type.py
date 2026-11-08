import os
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.category_page import CategoryPage

from config.config import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    EVENT_URL
)


def test_change_category_type(driver):

    assert ADMIN_EMAIL, "Email is missing"
    assert ADMIN_PASSWORD, "Password is missing"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    category_name = f"QA Category Type Test {timestamp}"

    # Login
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)

    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            "Your upcoming events"
        )
    )

    category_page = CategoryPage(driver)

    # Open categories
    category_page.open_category_page(
        f"{EVENT_URL}categories/"
    )

    # Open create category form
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(
            CategoryPage.CREATE_CATEGORY_LINK
        )
    )

    category_page.click_create_category()

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            CategoryPage.CATEGORY_NAME
        )
    )

    # Create a normal category
    category_page.enter_category_name(category_name)

    category_page.enter_category_description(
        "Category created for category type testing."
    )

    category_page.select_category_type("normal")

    category_page.save_category()

    # Wait for category to appear
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            category_name
        )
    )

    # Open category edit page
    category_page.click_edit_category_by_name(
        category_name
    )

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            CategoryPage.CATEGORY_NAME
        )
    )

    # Change category type to Add-on
    category_page.select_category_type("addon")

    category_page.save_category_changes()

    # Wait for category to appear after saving
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            category_name
        )
    )

    # Reopen category edit page
    category_page.click_edit_category_by_name(
        category_name
    )

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            CategoryPage.ADDON_CATEGORY
        )
    )

    # Verify saved category type
    addon_selected = driver.find_element(
        *CategoryPage.ADDON_CATEGORY
    ).is_selected()

    print("\nCategory:", category_name)
    print("Expected type: Add-on")
    print("Add-on radio selected:", addon_selected)
    print("Current URL:", driver.current_url)

    assert addon_selected, (
        "Category type was not changed to Add-on."
    )

    # Screenshot
    os.makedirs("screenshots", exist_ok=True)

    driver.save_screenshot(
        "screenshots/change_category_type.png"
    )