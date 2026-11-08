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


def test_create_product_with_duplicate_name(driver):

    assert ADMIN_EMAIL, "Email is missing"
    assert ADMIN_PASSWORD, "Password is missing"

    wait = WebDriverWait(driver, 20)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    product_name = f"QA Duplicate Product {timestamp}"
    product_price = "25.00"

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

    # Create the first product
    product_page.open_create_product_page(
        f"{EVENT_URL}items/add"
    )

    wait.until(
        EC.visibility_of_element_located(
            ProductPage.PRODUCT_NAME
        )
    )

    product_page.enter_product_name(product_name)
    product_page.enter_default_price(product_price)
    product_page.save_product()

    wait.until(
        EC.url_matches(r".*/items/\d+/$")
    )

    print("\nFirst product created:", product_name)

    # Create the second product using the same name
    product_page.open_create_product_page(
        f"{EVENT_URL}items/add"
    )

    wait.until(
        EC.visibility_of_element_located(
            ProductPage.PRODUCT_NAME
        )
    )

    product_page.enter_product_name(product_name)
    product_page.enter_default_price(product_price)
    product_page.save_product()

    # Wait for the second product to be created
    wait.until(
        EC.url_matches(r".*/items/\d+/$")
    )

    print("Second product created with the same name.")

    # Open product list
    product_page.open_product_list_page(
        f"{EVENT_URL}items/"
    )

    wait.until(
        EC.presence_of_element_located(
            ProductPage.PRODUCT_ROWS
        )
    )

    # Find products with the same name
    matching_products = []

    rows = product_page.find_elements(
        ProductPage.PRODUCT_ROWS
    )

    for row in rows:
        name_element = row.find_element(
            By.CSS_SELECTOR,
            "td strong a"
        )

        if name_element.text.strip() == product_name:
            matching_products.append(name_element.text.strip())

    print(
        "\nNumber of products with the same name:",
        len(matching_products)
    )

    # Verify that both products exist
    assert len(matching_products) == 2, (
        f"Expected 2 products with the name '{product_name}', "
        f"but found {len(matching_products)}"
    )

    print("\nBoth products with the same name were created successfully.")