import re
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.quota_page import QuotaPage

from config.config import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    EVENT_URL
)


def test_create_quota_with_zero_capacity(driver):

    assert ADMIN_EMAIL, "Email is missing"
    assert ADMIN_PASSWORD, "Password is missing"

    wait = WebDriverWait(driver, 20)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    product_name = f"QA Zero Quota Product {timestamp}"
    quota_name = f"QA Zero Capacity Quota {timestamp}"

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

    # Create a new product
    product_page.open_create_product_page(
        f"{EVENT_URL}items/add"
    )

    wait.until(
        EC.visibility_of_element_located(
            ProductPage.PRODUCT_NAME
        )
    )

    product_page.enter_product_name(product_name)
    product_page.enter_default_price("30.00")
    product_page.save_product()

    wait.until(
        EC.url_matches(r".*/items/\d+/$")
    )

    print("\nCreated product:", product_name)

    # Open product list
    product_page.open_product_list_page(
        f"{EVENT_URL}items/"
    )

    wait.until(
        EC.presence_of_element_located(
            ProductPage.PRODUCT_ROWS
        )
    )

    # Open the newly created product
    product_page.click_product_by_name(product_name)

    wait.until(
        EC.url_matches(r".*/items/\d+/$")
    )

    # Get product ID
    product_match = re.search(
        r"/items/(\d+)/",
        driver.current_url
    )

    assert product_match, "Product ID was not found."

    product_id = product_match.group(1)

    print("Selected product ID:", product_id)

    # Open Create Quota page
    quota_page = QuotaPage(driver)
    quota_page.click_create_quota()

    wait.until(
        EC.visibility_of_element_located(
            QuotaPage.QUOTA_NAME
        )
    )

    print("Create quota page opened.")

    # Enter quota information
    quota_page.enter_quota_name(quota_name)
    quota_page.enter_quota_size("0")

    # Assign product
    quota_page.select_product(product_id)

    selected_product = driver.find_element(
        By.CSS_SELECTOR,
        f'input[name="itemvars"][value="{product_id}"]'
    )

    assert selected_product.is_selected()

    # Save quota
    quota_page.save_quota()

    wait.until(
        EC.url_to_be(f"{EVENT_URL}quotas/")
    )

    wait.until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            "The new quota has been created."
        )
    )

    print("\nQuota creation confirmation received.")

    # Find the newly created quota
    quota_rows = quota_page.get_quota_rows()

    matching_quota = None

    for row in quota_rows:
        if quota_name in row.text:
            matching_quota = row
            break

    assert matching_quota is not None, (
        f"Quota was not found: {quota_name}"
    )

    print("Quota row:", matching_quota.text)

    # Verify quota information
    assert quota_name in matching_quota.text
    assert product_name in matching_quota.text

    # Verify zero total capacity and zero capacity left
    assert re.search(
        r"\b0\s+Sold out\b",
        matching_quota.text
    ), "Zero-capacity quota was not displayed as sold out."
    
    print("\nTC18 PASSED: Zero-capacity quota created successfully.")