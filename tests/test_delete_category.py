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


def test_delete_category(driver):

    assert ADMIN_EMAIL, "Email is missing"
    assert ADMIN_PASSWORD, "Password is missing"

    wait = WebDriverWait(driver, 20)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    category_name = f"QA Delete Category {timestamp}"

    # Login
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)

    wait.until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            "Your upcoming events"
        )
    )

    category_page = CategoryPage(driver)

    # Open categories page
    category_page.open_category_page(
        f"{EVENT_URL}categories/"
    )

    # Open create category form
    wait.until(
        EC.element_to_be_clickable(
            CategoryPage.CREATE_CATEGORY_LINK
        )
    )

    category_page.click_create_category()

    wait.until(
        EC.visibility_of_element_located(
            CategoryPage.CATEGORY_NAME
        )
    )

    # Create category for deletion testing
    category_page.enter_category_name(category_name)

    category_page.enter_category_description(
        "Temporary category created for deletion testing."
    )

    category_page.save_category()

    # Verify category was created
    wait.until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            category_name
        )
    )

    # Find the category and click its Delete button
    category_page.click_delete_category_by_name(
        category_name
    )

    # Wait for confirmation page
    wait.until(
        EC.url_contains("/delete")
    )

    # Verify confirmation page
    confirmation_text = driver.find_element(
        By.TAG_NAME,
        "body"
    ).text

    assert category_name in confirmation_text

    # Click confirmation Delete button
    delete_confirmation_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "button.btn-danger.btn-save"
            )
        )
    )

    delete_confirmation_button.click()

    # Wait until Pretix returns to the category list
    wait.until(
        EC.url_to_be(
            f"{EVENT_URL}categories/"
        )
    )

    # Verify category has been deleted
    wait.until_not(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            category_name
        )
    )

    body_text = driver.find_element(
        By.TAG_NAME,
        "body"
    ).text

    print("\nDeleted category:", category_name)
    print("Current URL:", driver.current_url)

    assert category_name not in body_text

    # Screenshot
    os.makedirs("screenshots", exist_ok=True)

    driver.save_screenshot(
        "screenshots/delete_category.png"
    )