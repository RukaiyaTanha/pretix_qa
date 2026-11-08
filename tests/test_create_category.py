
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


def test_create_category(driver):

    assert ADMIN_EMAIL, "Email is missing"
    assert ADMIN_PASSWORD, "Password is missing"

    # Generate a unique category name for every test run
    category_name = (
        f"QA Automation Category "
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )

    category_description = (
        "Category created through Selenium automation."
    )

    # Step 1: Login
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)

    WebDriverWait(driver, 15).until(
        EC.text_to_be_present_in_element(
        (By.TAG_NAME, "body"),
        "Your upcoming events"
       )
    )

    # Step 2: Open category list
    category_page = CategoryPage(driver)

    category_url = f"{EVENT_URL}categories/"
    category_page.open_category_page(category_url)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'a[href$="/categories/add"]')
        )
    )

    # Step 3: Click Create a new category
    category_page.click_create_category()

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            CategoryPage.CATEGORY_NAME
        )
    )

    # Step 4: Enter category information
    category_page.enter_category_name(category_name)

    category_page.enter_category_description(
        category_description
    )

    # Step 5: Select category type
    category_page.select_category_type("normal")

    # Step 6: Save category
    category_page.save_category()

    # Step 7: Wait for the new category to appear
    WebDriverWait(driver, 15).until(
        EC.text_to_be_present_in_element(
        (By.TAG_NAME, "body"),
        category_name
        )
    )

    # Step 8: Verify category creation
    body_text = driver.find_element(
        By.TAG_NAME, "body"
    ).text

    print("\nCreated category:", category_name)
    print("Current URL:", driver.current_url)

    assert category_name in body_text

    # Screenshot
    os.makedirs("screenshots", exist_ok=True)
    driver.save_screenshot(
        "screenshots/create_category.png"
    )
