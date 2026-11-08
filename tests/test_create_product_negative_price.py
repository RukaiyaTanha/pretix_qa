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


def test_create_product_with_negative_price(driver):

    assert ADMIN_EMAIL, "Email is missing"
    assert ADMIN_PASSWORD, "Password is missing"

    wait = WebDriverWait(driver, 20)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    product_name = f"QA Negative Price Product {timestamp}"

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

    # Enter valid product name
    product_page.enter_product_name(product_name)

    # Enter negative default price
    product_page.enter_default_price("-10.00")

    # Verify entered values
    name_value = driver.find_element(
        *ProductPage.PRODUCT_NAME
    ).get_attribute("value")

    price_value = driver.find_element(
        *ProductPage.DEFAULT_PRICE
    ).get_attribute("value")

    assert name_value == product_name
    assert price_value == "-10.00"

    print("\nProduct name:", name_value)
    print("Entered price:", price_value)

    # Submit product form
    product_page.save_product()

    # Wait for the result
    wait.until(
        lambda d: (
            "/items/add" in d.current_url
            or "/items/" in d.current_url
        )
    )

    current_url = driver.current_url

    print("Current URL after submission:", current_url)

    # Check whether the product was rejected
    if "/items/add" in current_url:

        body_text = driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        print("Form validation response:", body_text)

        print("Negative price submission was rejected.")

    else:

        body_text = driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        print("Product creation response:", body_text)

        assert product_name not in body_text, (
            "Product may have been created with a negative price. "
            "Investigate the saved product before reporting a defect."
        )

    # Screenshot
    os.makedirs("screenshots", exist_ok=True)

    driver.save_screenshot(
        "screenshots/create_product_negative_price.png"
    )