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


def test_open_product_list(driver):

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

    # Open product list
    product_page.open_product_list_page(
        f"{EVENT_URL}items/"
    )

    # Wait for product list heading
    wait.until(
        EC.visibility_of_element_located(
            ProductPage.PRODUCT_LIST_HEADING
        )
    )

    # Verify URL
    assert "/items/" in driver.current_url

    # Verify heading
    heading = product_page.get_product_list_heading()

    print("\nProduct list heading:", heading)
    print("Current URL:", driver.current_url)

    assert heading == "Products"

    # Verify Create a new product link
    assert product_page.is_create_product_link_visible(), (
        "Create a new product link is not visible."
    )

    print("Create product link is visible.")

    # Screenshot
    import os
    os.makedirs("screenshots", exist_ok=True)

    driver.save_screenshot(
        "screenshots/open_product_list.png"
    )