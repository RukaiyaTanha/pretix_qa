from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.quota_page import QuotaPage

from config.config import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    EVENT_URL
)


def test_open_quota_page(driver):

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

    quota_page = QuotaPage(driver)

    # Open Quotas page
    quota_page.open_quota_page(
        f"{EVENT_URL}quotas/"
    )

    wait.until(
        EC.visibility_of_element_located(
            QuotaPage.QUOTA_HEADING
        )
    )

    # Verify heading
    heading = quota_page.get_quota_heading()

    print("\nPage heading:", heading)

    assert heading == "Quotas"

    # Verify quota list
    wait.until(
        EC.presence_of_element_located(
            QuotaPage.QUOTA_ROWS
        )
    )

    quota_rows = quota_page.get_quota_rows()

    print("Number of quota rows:", len(quota_rows))

    assert len(quota_rows) > 0, (
        "No quotas are displayed."
    )

    print("\nQuota management page opened successfully.")