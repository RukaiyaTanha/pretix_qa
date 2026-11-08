
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CategoryPage(BasePage):

    # Category list
    CATEGORY_HEADING = (By.TAG_NAME, "h1")

    CREATE_CATEGORY_LINK = (
        By.CSS_SELECTOR,
        'a[href$="/categories/add"]'
    )

    # Category form
    CATEGORY_NAME = (By.ID, "id_name_0")

    CATEGORY_DESCRIPTION = (
        By.ID,
        "id_description_0"
    )

    # Category type radio buttons
    NORMAL_CATEGORY = (
        By.ID,
        "id_category_type_0"
    )

    ADDON_CATEGORY = (
        By.ID,
        "id_category_type_1"
    )

    CROSS_SELLING_CATEGORY = (
        By.ID,
        "id_category_type_2"
    )

    NORMAL_CROSS_SELLING_CATEGORY = (
        By.ID,
        "id_category_type_3"
    )

    SAVE_BUTTON = (
        By.CSS_SELECTOR,
        "button.btn-save"
    )

    def open_category_page(self, url):
        self.open(url)

    def get_heading(self):
        return self.find_element(self.CATEGORY_HEADING).text

    def click_create_category(self):
        self.find_element(self.CREATE_CATEGORY_LINK).click()

    def enter_category_name(self, name):
        field = self.find_element(self.CATEGORY_NAME)
        field.clear()
        field.send_keys(name)

    def enter_category_description(self, description):
        field = self.find_element(self.CATEGORY_DESCRIPTION)
        field.clear()
        field.send_keys(description)

    def select_category_type(self, category_type="normal"):

        category_types = {
            "normal": self.NORMAL_CATEGORY,
            "addon": self.ADDON_CATEGORY,
            "only": self.CROSS_SELLING_CATEGORY,
            "both": self.NORMAL_CROSS_SELLING_CATEGORY
        }

        if category_type not in category_types:
            raise ValueError(
                f"Invalid category type: {category_type}"
            )

        self.find_element(
            category_types[category_type]
        ).click()

    def save_category(self):
        self.find_element(self.SAVE_BUTTON).click()

    def get_category_name_validation_message(self):
        field = self.find_element(self.CATEGORY_NAME)
        return field.get_attribute("validationMessage")

    # Category list
    CATEGORY_ROWS = (
        By.CSS_SELECTOR,
        "tr"
    )

    EDIT_CATEGORY_BUTTON = (
        By.CSS_SELECTOR,
        'a[title="Edit"]'
    )

    def click_edit_category_by_name(self, category_name):
        rows = self.find_elements(self.CATEGORY_ROWS)

        for row in rows:
            if category_name in row.text:
                edit_button = row.find_element(
                    *self.EDIT_CATEGORY_BUTTON
                )
                edit_button.click()
                return

        raise AssertionError(
            f"Category not found: {category_name}"
        )

    def update_category_name(self, new_name):
        field = self.find_element(self.CATEGORY_NAME)
        field.clear()
        field.send_keys(new_name)

    def save_category_changes(self):
        self.find_element(self.SAVE_BUTTON).click()

    DELETE_CATEGORY_BUTTON = (
        By.CSS_SELECTOR,
       'a[title="Delete"]'
    )

    def click_delete_category_by_name(self, category_name):
        rows = self.find_elements(
           self.CATEGORY_ROWS
        )
        for row in rows:
            if category_name in row.text:
                delete_button = row.find_element(
                    *self.DELETE_CATEGORY_BUTTON
                )
                delete_button.click()
                return

        raise AssertionError(
            f"Category not found: {category_name}"
        )