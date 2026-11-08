import os
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.product_page import ProductPage

from config.config import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    EVENT_URL
)


def test_edit_product(driver):

    assert ADMIN_EMAIL, "Email is missing"
    assert ADMIN_PASSWORD, "Password is missing"

    product_name = (
        f"QA Edit Test Product "
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )

    updated_name = (
        f"QA Updated Product "
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )

    product_description = (
        "Product created for edit automation testing."
    )

    updated_description = (
        "Product updated through Selenium automation."
    )

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

    product_page = ProductPage(driver)

    # Create a product for this test
    product_page.open_create_product_page(
        f"{EVENT_URL}items/add"
    )

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            ProductPage.PRODUCT_NAME
        )
    )

    product_page.enter_product_name(product_name)
    product_page.enter_default_price("10.00")
    product_page.save_product()

    # Wait for the product to be saved
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            product_name
        )
    )

    # Open product list
    product_page.open_create_product_page(
        f"{EVENT_URL}items/"
    )

    WebDriverWait(driver, 15).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            product_name
        )
    )

    # Find product by name and click its Edit button
    product_page.click_edit_product_by_name(
        product_name
    )

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            ProductPage.PRODUCT_NAME
        )
    )

    # Update General information
    product_page.update_product_name(updated_name)

    product_page.update_product_description(
        updated_description
    )

    product_page.save_product_changes()

    # Verify updated product
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

    print("\nOriginal product:", product_name)
    print("Updated product:", updated_name)
    print("Current URL:", driver.current_url)

    assert updated_name in body_text

    os.makedirs("screenshots", exist_ok=True)

    driver.save_screenshot(
        "screenshots/edit_product.png"
    )