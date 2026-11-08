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


def test_delete_unused_product(driver):

    assert ADMIN_EMAIL, "Email is missing"
    assert ADMIN_PASSWORD, "Password is missing"

    wait = WebDriverWait(driver, 20)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    product_name = f"QA Delete Product {timestamp}"

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

    # Create a product for deletion
    product_page.open_create_product_page(
        f"{EVENT_URL}items/add"
    )

    wait.until(
        EC.visibility_of_element_located(
            ProductPage.PRODUCT_NAME
        )
    )

    product_page.enter_product_name(product_name)
    product_page.enter_default_price("20.00")
    product_page.save_product()

    wait.until(
        EC.url_matches(r".*/items/\d+/$")
    )

    print("\nCreated product:", product_name)

    # Open all products
    product_page.open_product_list_page(
        f"{EVENT_URL}items/"
    )

    wait.until(
        EC.presence_of_element_located(
            ProductPage.PRODUCT_ROWS
        )
    )

    # Find the product and click Delete directly
    product_page.click_delete_product_by_name(
        product_name
    )

    # Wait for deletion confirmation page
    wait.until(
        EC.url_contains("/delete")
    )

    print("Opened product deletion page.")

    # Confirm deletion
    wait.until(
        EC.element_to_be_clickable(
            ProductPage.CONFIRM_DELETE_BUTTON
        )
    )

    product_page.confirm_delete_product()

    # Wait for product list
    wait.until(
        EC.url_to_be(f"{EVENT_URL}items/")
    )

    print("Product deletion confirmed.")

    # Verify product is removed
    rows = product_page.find_elements(
        ProductPage.PRODUCT_ROWS
    )

    remaining_products = [
        row.text
        for row in rows
        if product_name in row.text
    ]

    assert not remaining_products, (
        f"Product still exists: {product_name}"
    )

    print("\nProduct successfully deleted.")