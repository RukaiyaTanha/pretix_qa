from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.category_page import CategoryPage

from config.config import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    EVENT_URL
)


def test_create_category_empty_name(driver):

    assert ADMIN_EMAIL, "Email is missing"
    assert ADMIN_PASSWORD, "Password is missing"

    # Login
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)

    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            "Your upcoming events"
        )
    )

    # Open category page
    category_page = CategoryPage(driver)

    category_url = f"{EVENT_URL}categories/"

    category_page.open_category_page(category_url)

    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(
            CategoryPage.CREATE_CATEGORY_LINK
        )
    )

    # Open create category form
    category_page.click_create_category()

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            CategoryPage.CATEGORY_NAME
        )
    )

    # Keep category name empty
    category_name = driver.find_element(
        *CategoryPage.CATEGORY_NAME
    )

    category_name.clear()

    # Submit form
    category_page.save_category()

    # Wait for the response
    WebDriverWait(driver, 15).until(
        lambda d: (
            d.current_url.endswith("/categories/add")
            or d.current_url.endswith("/categories/")
        )
    )

    # Inspect validation response
    body_text = driver.find_element(
        By.TAG_NAME,
        "body"
    ).text

    print("\nCurrent URL:", driver.current_url)
    print("Page response:", body_text)

    # Verify category was not created
    assert driver.current_url.endswith("/categories/add"), (
        "The form did not remain on the category creation page."
    )

    print("\nEmpty category name was rejected successfully.")