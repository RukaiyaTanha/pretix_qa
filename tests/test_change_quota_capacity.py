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


def test_change_quota_capacity(driver):

    wait = WebDriverWait(driver, 20)

    # --------------------------------------------------
    # Step 1: Login
    # --------------------------------------------------

    assert ADMIN_EMAIL, "Admin email is missing."
    assert ADMIN_PASSWORD, "Admin password is missing."

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
    quota_page = QuotaPage(driver)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # --------------------------------------------------
    # Step 2: Create a product
    # --------------------------------------------------

    product_name = f"QA TC20 Capacity Product {timestamp}"

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

    print(f"Created product: {product_name}")

    # --------------------------------------------------
    # Step 3: Open the product
    # --------------------------------------------------

    product_page.open_product_list_page(
        f"{EVENT_URL}items/"
    )

    wait.until(
        EC.presence_of_element_located(
            ProductPage.PRODUCT_ROWS
        )
    )

    product_page.click_product_by_name(product_name)

    wait.until(
        EC.url_matches(r".*/items/\d+/$")
    )

    # --------------------------------------------------
    # Step 4: Create a quota with capacity 50
    # --------------------------------------------------

    quota_name = f"QA TC20 Capacity Quota {timestamp}"

    quota_page.click_create_quota()

    wait.until(
        EC.visibility_of_element_located(
            QuotaPage.QUOTA_NAME
        )
    )

    quota_page.enter_quota_name(quota_name)
    quota_page.enter_quota_size("50")

    quota_page.save_quota()

    wait.until(
        EC.url_to_be(f"{EVENT_URL}quotas/")
    )

    wait.until(
        EC.presence_of_element_located(
            QuotaPage.QUOTA_ROWS
        )
    )

    print(f"Created quota: {quota_name}")
    print("Initial capacity: 50")

    # --------------------------------------------------
    # Step 5: Open the quota for editing
    # --------------------------------------------------

    quota_page.click_edit_quota_by_name(quota_name)

    wait.until(
        EC.visibility_of_element_located(
            QuotaPage.QUOTA_SIZE
        )
    )

    # Verify the initial capacity.
    initial_capacity = quota_page.get_quota_size()

    assert initial_capacity == "50", (
        f"Expected initial capacity 50, "
        f"but found {initial_capacity}."
    )

        # --------------------------------------------------
    # Step 6: Change capacity from 50 to 75
    # --------------------------------------------------

    quota_page.enter_quota_size("75")
    quota_page.save_quota()

    # Wait for the save operation to finish.
    wait.until(
        lambda d: (
            "75" in d.find_element(
                By.TAG_NAME,
                "body"
            ).text
            or d.current_url.endswith("/quotas/")
        )
    )

    print(f"After saving, current URL: {driver.current_url}")

    # --------------------------------------------------
    # Step 7: Open the quota list
    # --------------------------------------------------

    quota_page.open_quota_page(
        f"{EVENT_URL}quotas/"
    )

    wait.until(
        EC.presence_of_element_located(
            QuotaPage.QUOTA_ROWS
        )
    )

    # --------------------------------------------------
    # Step 8: Reopen the quota and verify
    # --------------------------------------------------

    quota_page.click_edit_quota_by_name(quota_name)

    wait.until(
        EC.visibility_of_element_located(
            QuotaPage.QUOTA_SIZE
        )
    )

    updated_capacity = quota_page.get_quota_size()

    assert updated_capacity == "75", (
        f"Quota capacity was not updated. "
        f"Expected 75, but found {updated_capacity}."
    )

    print(f"Verified updated capacity: {updated_capacity}")
    print("TC20 PASSED")