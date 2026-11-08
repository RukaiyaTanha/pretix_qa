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


def test_create_quota_with_valid_capacity(driver):

    assert ADMIN_EMAIL, "Email is missing"
    assert ADMIN_PASSWORD, "Password is missing"

    wait = WebDriverWait(driver, 20)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    product_name = f"QA Quota Product {timestamp}"
    quota_name = f"QA Valid Quota {timestamp}"

    product_price = "30.00"
    quota_capacity = "50"

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
    product_page.enter_default_price(product_price)
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

    # Select the newly created product
    product_page.click_product_by_name(
        product_name
    )

    wait.until(
        EC.url_matches(r".*/items/\d+/$")
    )

    # Get dynamic product ID
    product_match = re.search(
        r"/items/(\d+)/",
        driver.current_url
    )

    assert product_match, "Product ID was not found."

    product_id = product_match.group(1)

    print("Selected product ID:", product_id)

    # Open Create Quota
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
    quota_page.enter_quota_size(quota_capacity)

    # Assign the selected product
    quota_page.select_product(product_id)

    # Verify selected product
    selected_product = driver.find_element(
        By.CSS_SELECTOR,
        f'input[name="itemvars"][value="{product_id}"]'
    )

    assert selected_product.is_selected(), (
        "The product was not selected for the quota."
    )

    # Save quota
    quota_page.save_quota()

    wait.until(
        EC.url_to_be(
            f"{EVENT_URL}quotas/"
        )
    )

    wait.until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            "The new quota has been created."
        )
    )

    print("\nQuota created:", quota_name)

    # Verify quota appears in the quota list
    quota_rows = quota_page.get_quota_rows()

    matching_quota = None

    for row in quota_rows:
        if quota_name in row.text:
            matching_quota = row
            break

    assert matching_quota is not None, (
        f"Created quota was not found: {quota_name}"
    )

    # Verify quota name
    assert quota_name in matching_quota.text

    # Verify assigned product
    assert product_name in matching_quota.text

    # Verify capacity
    assert quota_capacity in matching_quota.text

    print("Verified quota name:", quota_name)
    print("Verified assigned product:", product_name)
    print("Verified capacity:", quota_capacity)

    print("\nTC17 PASSED: Quota created with valid capacity.")