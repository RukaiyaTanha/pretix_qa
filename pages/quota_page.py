from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class QuotaPage(BasePage):

    QUOTA_HEADING = (
        By.TAG_NAME,
        "h1"
    )

    QUOTA_ROWS = (
        By.CSS_SELECTOR,
        "table tbody tr"
    )

    CREATE_QUOTA_BUTTON = (
        By.CSS_SELECTOR,
        'a[href*="/quotas/add?product="]'
    )

    QUOTA_NAME = (
        By.ID,
        "id_name"
    )

    QUOTA_SIZE = (
        By.ID,
        "id_size"
    )

    PRODUCT_CHECKBOXES = (
        By.CSS_SELECTOR,
        'input[name="itemvars"]'
    )

    SAVE_BUTTON = (
        By.CSS_SELECTOR,
        "button.btn-save"
    )

    def open_quota_page(self, url):
        self.open(url)

    def get_quota_heading(self):
        return self.find_element(
            self.QUOTA_HEADING
        ).text

    def get_quota_rows(self):
        return self.find_elements(
            self.QUOTA_ROWS
        )

    def click_create_quota(self):
        self.find_element(
            self.CREATE_QUOTA_BUTTON
        ).click()

    def enter_quota_name(self, name):
        field = self.find_element(self.QUOTA_NAME)
        field.clear()
        field.send_keys(name)

    def enter_quota_size(self, size):
        field = self.find_element(self.QUOTA_SIZE)
        field.clear()
        field.send_keys(size)

    def select_product(self, product_id):

        checkbox = self.driver.find_element(
            By.CSS_SELECTOR,
            f'input[name="itemvars"][value="{product_id}"]'
        )

        if not checkbox.is_selected():
            checkbox.click()

    def save_quota(self):
        self.find_element(self.SAVE_BUTTON).click()

    def get_quota_name(self):
        return self.find_element(
            self.QUOTA_NAME
        ).get_attribute("value")

    def get_quota_size(self):
        return self.find_element(
            self.QUOTA_SIZE
        ).get_attribute("value")

    EDIT_QUOTA_BUTTON = (
        By.CSS_SELECTOR,
        'a[href$="/change"]'
    )

    QUOTA_NAME_LINK = (
        By.CSS_SELECTOR,
        "td strong a"
    )

    def click_edit_quota_by_name(self, quota_name):

        rows = self.find_elements(self.QUOTA_ROWS)

        for row in rows:

            if quota_name in row.text:

                edit_button = row.find_element(
                    *self.EDIT_QUOTA_BUTTON
                )

                edit_button.click()
                return

        raise AssertionError(
            f"Quota not found: {quota_name}"
        )

    def unselect_product(self, product_id):

        checkbox = self.driver.find_element(
            By.CSS_SELECTOR,
            f'input[name="itemvars"][value="{product_id}"]'
        )

        if checkbox.is_selected():
            checkbox.click()