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


def test_create_product(driver):

    assert ADMIN_EMAIL, "Email is missing"
    assert ADMIN_PASSWORD, "Password is missing"

    product_name = (
        f"QA Automation Product "
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )

    product_price = "10.00"

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

    # Open product creation page
    product_page = ProductPage(driver)

    create_product_url = f"{EVENT_URL}items/add"

    product_page.open_create_product_page(
        create_product_url
    )

    # Wait for product form
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            ProductPage.PRODUCT_NAME
        )
    )

    # Fill product information
    product_page.enter_product_name(product_name)
    product_page.enter_default_price(product_price)

    # Save product
    product_page.save_product()

    # Verify product creation
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            product_name
        )
    )

    body_text = driver.find_element(
        By.TAG_NAME,
        "body"
    ).text

    print("\nCreated product:", product_name)
    print("Product price:", product_price)
    print("Current URL:", driver.current_url)

    assert product_name in body_text

    os.makedirs("screenshots", exist_ok=True)
    driver.save_screenshot(
        "screenshots/create_product.png"
    )