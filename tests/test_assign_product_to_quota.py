import re
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.quota_page import QuotaPage

from config.config import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    EVENT_URL
)


def test_assign_additional_product_to_existing_quota(driver):

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
    # Step 2: Create the first product
    # This product will initially belong to the quota.
    # --------------------------------------------------

    product_a_name = f"QA TC19 Product A {timestamp}"

    product_page.open_create_product_page(
        f"{EVENT_URL}items/add"
    )

    wait.until(
        EC.visibility_of_element_located(
            ProductPage.PRODUCT_NAME
        )
    )

    product_page.enter_product_name(product_a_name)
    product_page.enter_default_price("30.00")
    product_page.save_product()

    wait.until(
        EC.url_matches(r".*/items/\d+/$")
    )

    match_a = re.search(
        r"/items/(\d+)/",
        driver.current_url
    )

    assert match_a, "Could not retrieve the first product ID."

    product_a_id = match_a.group(1)

    print(f"Created first product: {product_a_name}")
    print(f"First product ID: {product_a_id}")

    # --------------------------------------------------
    # Step 3: Create the second product
    # This product will be added to the existing quota.
    # --------------------------------------------------

    product_b_name = f"QA TC19 Product B {timestamp}"

    product_page.open_create_product_page(
        f"{EVENT_URL}items/add"
    )

    wait.until(
        EC.visibility_of_element_located(
            ProductPage.PRODUCT_NAME
        )
    )

    product_page.enter_product_name(product_b_name)
    product_page.enter_default_price("40.00")
    product_page.save_product()

    wait.until(
        EC.url_matches(r".*/items/\d+/$")
    )

    match_b = re.search(
        r"/items/(\d+)/",
        driver.current_url
    )

    assert match_b, "Could not retrieve the second product ID."

    product_b_id = match_b.group(1)

    print(f"Created second product: {product_b_name}")
    print(f"Second product ID: {product_b_id}")

    # --------------------------------------------------
    # Step 4: Open the first product
    # --------------------------------------------------

    product_page.open_product_list_page(
        f"{EVENT_URL}items/"
    )

    wait.until(
        EC.presence_of_element_located(
            ProductPage.PRODUCT_ROWS
        )
    )

    product_page.click_product_by_name(product_a_name)

    wait.until(
        EC.url_matches(r".*/items/\d+/$")
    )

    # --------------------------------------------------
    # Step 5: Create a new quota for the first product
    # --------------------------------------------------

    quota_name = f"QA TC19 Quota {timestamp}"

    quota_page.click_create_quota()

    wait.until(
        EC.visibility_of_element_located(
            QuotaPage.QUOTA_NAME
        )
    )

    quota_page.enter_quota_name(quota_name)
    quota_page.enter_quota_size("50")

    # Ensure Product A is assigned to this quota.
    quota_page.select_product(product_a_id)

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

    # --------------------------------------------------
    # Step 6: Open the existing quota for editing
    # --------------------------------------------------

    quota_page.click_edit_quota_by_name(quota_name)

    wait.until(
        EC.visibility_of_element_located(
            QuotaPage.QUOTA_NAME
        )
    )

        # --------------------------------------------------
    # Step 7: Assign the second product to the quota
    # --------------------------------------------------

    quota_page.select_product(product_b_id)

    edit_url = driver.current_url

    quota_page.save_quota()

    # Check whether Pretix redirects after saving.
    try:
        wait.until(
            lambda d: d.current_url != edit_url
        )

        print("Quota edit submitted successfully.")
        print(f"Redirected URL: {driver.current_url}")

    except TimeoutException:

        print("The page did not redirect after saving.")
        print(f"Current URL: {driver.current_url}")

        print("Page content:")
        print(
            driver.find_element(
                By.TAG_NAME,
                "body"
            ).text
        )

        raise

    # Open the quota list explicitly.
    quota_page.open_quota_page(
        f"{EVENT_URL}quotas/"
    )

    wait.until(
        EC.presence_of_element_located(
            QuotaPage.QUOTA_ROWS
        )
    )

    # --------------------------------------------------
    # Step 8: Verify both products are assigned
    # --------------------------------------------------

    matching_row = None

    for row in quota_page.get_quota_rows():

        if quota_name in row.text:
            matching_row = row
            break

    assert matching_row is not None, (
        f"Quota was not found after editing: {quota_name}"
    )

    quota_text = matching_row.text

    assert product_a_name in quota_text, (
        "The original product is missing from the quota."
    )

    assert product_b_name in quota_text, (
        "The additional product was not assigned to the quota."
    )

    assert "50" in quota_text, (
        "The quota capacity was not preserved."
    )

    print("Both products are assigned to the existing quota.")
    print(f"Quota name: {quota_name}")
    print("Quota capacity: 50")
    print("TC19 PASSED")