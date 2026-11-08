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


def test_create_product_without_name(driver):

    assert ADMIN_EMAIL, "Email is missing"
    assert ADMIN_PASSWORD, "Password is missing"

    wait = WebDriverWait(driver, 20)

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

    product_page = ProductPage(driver)

    # Open create product page
    product_page.open_create_product_page(
        f"{EVENT_URL}items/add"
    )

    wait.until(
        EC.visibility_of_element_located(
            ProductPage.PRODUCT_NAME
        )
    )

    # Leave product name empty
    name_field = driver.find_element(
        *ProductPage.PRODUCT_NAME
    )

    assert name_field.get_attribute("value") == ""

    # Click Save without entering a product name
    product_page.save_product()

    # Verify form remains open
    wait.until(
        EC.visibility_of_element_located(
            ProductPage.PRODUCT_NAME
        )
    )

    current_url = driver.current_url

    name_value = driver.find_element(
        *ProductPage.PRODUCT_NAME
    ).get_attribute("value")

    print("\nCurrent URL:", current_url)
    print("Product name value:", name_value)

    assert "/items/add" in current_url, (
        "The application left the creation page unexpectedly."
    )

    assert name_value == "", (
        "Product name should remain empty."
    )

    print("Empty product name was not accepted.")

    # Screenshot
    import os
    os.makedirs("screenshots", exist_ok=True)

    driver.save_screenshot(
        "screenshots/create_product_empty_name.png"
    )