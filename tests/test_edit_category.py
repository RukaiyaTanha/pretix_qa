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


def test_edit_category(driver):

    assert ADMIN_EMAIL, "Email is missing"
    assert ADMIN_PASSWORD, "Password is missing"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    original_name = f"QA Edit Category {timestamp}"
    updated_name = f"QA Updated Category {timestamp}"

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

    # Create category for this test
    category_page.enter_category_name(original_name)
    category_page.enter_category_description(
        "Category created for edit automation testing."
    )

    category_page.save_category()

    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            original_name
        )
    )

    # Locate category and open its edit page
    category_page.click_edit_category_by_name(
        original_name
    )

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            CategoryPage.CATEGORY_NAME
        )
    )

    # Update category name
    category_page.update_category_name(updated_name)

    category_page.save_category_changes()

    # Verify updated category name
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            updated_name
        )
    )

    body_text = driver.find_element(
        By.TAG_NAME,
        "body"
    ).text

    print("\nOriginal category:", original_name)
    print("Updated category:", updated_name)
    print("Current URL:", driver.current_url)

    assert updated_name in body_text
    assert original_name not in body_text

    os.makedirs("screenshots", exist_ok=True)

    driver.save_screenshot(
        "screenshots/edit_category.png"
    )