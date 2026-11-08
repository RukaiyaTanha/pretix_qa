
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


def test_edit_product_price(driver):

    assert ADMIN_EMAIL, "Email is missing"
    assert ADMIN_PASSWORD, "Password is missing"

    wait = WebDriverWait(driver, 20)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    product_name = f"QA Price Edit Product {timestamp}"

    initial_price = "30.00"
    updated_price = "50.00"

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

    # Create a new product
    product_page.enter_product_name(product_name)
    product_page.enter_default_price(initial_price)

    product_page.save_product()

    # Wait until the product is created
    wait.until(
        EC.url_matches(r".*/items/\d+/$")
    )

    print("\nCreated product:", product_name)
    print("Initial price:", initial_price)

    # Return to product list
    product_page.open_product_list_page(
        f"{EVENT_URL}items/"
    )

    wait.until(
        EC.presence_of_element_located(
            ProductPage.PRODUCT_ROWS
        )
    )

    # Find and edit the newly created product
    product_page.click_edit_product_by_name(
        product_name
    )

    wait.until(
        EC.url_matches(r".*/items/\d+/$")
    )

    # Open Price tab
    product_page.click_price_tab()

    wait.until(
        EC.visibility_of_element_located(
            ProductPage.DEFAULT_PRICE
        )
    )

    # Verify original price
    original_price = product_page.get_product_price()

    print("Verified original price:", original_price)

    assert original_price == initial_price, (
        f"Expected initial price {initial_price}, "
        f"but found {original_price}"
    )

    # Update product price
    product_page.update_product_price(
        updated_price
    )

    entered_price = product_page.get_product_price()

    assert entered_price == updated_price

    print("Updated price entered:", entered_price)

    # Save changes
    product_page.save_product_changes()

    wait.until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            "Your changes have been saved."
        )
    )

    # Reopen Price tab and verify saved price
    product_page.click_price_tab()

    wait.until(
        EC.visibility_of_element_located(
            ProductPage.DEFAULT_PRICE
        )
    )

    saved_price = product_page.get_product_price()

    print("Saved price:", saved_price)

    assert saved_price == updated_price, (
        f"Expected saved price {updated_price}, "
        f"but found {saved_price}"
    )

    print("\nProduct price updated successfully.")
