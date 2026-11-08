from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductPage(BasePage):

    # Product form locators
    PRODUCT_NAME = (
        By.ID,
        "id_name_0"
    )

    DEFAULT_PRICE = (
        By.ID,
        "id_default_price"
    )

    SAVE_BUTTON = (
        By.CSS_SELECTOR,
        "button.btn-save"
    )

    CREATE_PRODUCT_LINK = (
        By.CSS_SELECTOR,
        'a[href="/control/event/qatesting/qa/items/add"]'
    )

    def open_create_product_page(self, url):
        self.open(url)

    def enter_product_name(self, name):
        field = self.find_element(self.PRODUCT_NAME)
        field.clear()
        field.send_keys(name)

    def enter_default_price(self, price):
        field = self.find_element(self.DEFAULT_PRICE)
        field.clear()
        field.send_keys(price)

    def save_product(self):
        self.find_element(self.SAVE_BUTTON).click()

    # Product list
    PRODUCT_ROWS = (
        By.CSS_SELECTOR,
        'tr[data-dnd-id]'
    )

    EDIT_BUTTON = (
        By.CSS_SELECTOR,
        'a[title="Edit"]'
    )

    def click_edit_product_by_name(self, product_name):

        rows = self.find_elements(self.PRODUCT_ROWS)

        for row in rows:
            if product_name in row.text:

                edit_button = row.find_element(
                    *self.EDIT_BUTTON
                )

                edit_button.click()
                return

        raise AssertionError(
            f"Product not found: {product_name}"
        )

    # General tab
    GENERAL_TAB = (
        By.CSS_SELECTOR,
        'a[href="#tab-0-0"]'
    )

    PRODUCT_DESCRIPTION = (
        By.ID,
        "id_description_0"
    )

    SAVE_EDIT_BUTTON = (
        By.CSS_SELECTOR,
        "button.btn-save"
    )

    def click_edit_product(self):
        self.find_element(self.EDIT_PRODUCT_BUTTON).click()

    def click_general_tab(self):
        self.find_element(self.GENERAL_TAB).click()

    def update_product_name(self, name):
        field = self.find_element(self.PRODUCT_NAME)
        field.clear()
        field.send_keys(name)

    def update_product_description(self, description):
        field = self.find_element(self.PRODUCT_DESCRIPTION)
        field.clear()
        field.send_keys(description)

    def save_product_changes(self):
        self.find_element(self.SAVE_EDIT_BUTTON).click()

    # Product list page
    PRODUCT_LIST_HEADING = (
        By.TAG_NAME,
        "h1"
    )

    PRODUCT_LIST_DESCRIPTION = (
        By.CSS_SELECTOR,
        ".page-header p"
    )

    def open_product_list_page(self, url):
        self.open(url)

    def get_product_list_heading(self):
        return self.find_element(
            self.PRODUCT_LIST_HEADING
        ).text

    def is_create_product_link_visible(self):
        return self.find_element(
            self.CREATE_PRODUCT_LINK
        ).is_displayed()

    # Price tab
    PRICE_TAB = (
        By.CSS_SELECTOR,
        'a[href="#tab-0-1"]'
    )

    def click_price_tab(self):
        self.find_element(self.PRICE_TAB).click()

    def update_product_price(self, price):
        field = self.find_element(self.DEFAULT_PRICE)
        field.clear()
        field.send_keys(price)

    def get_product_price(self):
        return self.find_element(
            self.DEFAULT_PRICE
        ).get_attribute("value")

    # Delete product

    DELETE_PRODUCT_BUTTON = (
        By.CSS_SELECTOR,
       'a[title="Delete"]'
    )

    CONFIRM_DELETE_BUTTON = (
        By.CSS_SELECTOR,
        "button.btn-danger.btn-save"
    )

    def click_delete_product_by_name(self, product_name):

        rows = self.find_elements(self.PRODUCT_ROWS)
        for row in rows:
            if product_name in row.text:
                delete_button = row.find_element(
                    *self.DELETE_PRODUCT_BUTTON
                )
                delete_button.click()
                return

        raise AssertionError(
            f"Product not found: {product_name}"
        )

    def confirm_delete_product(self):

        self.find_element(
            self.CONFIRM_DELETE_BUTTON
        ).click()


    def click_product_by_name(self, product_name):
        rows = self.find_elements(self.PRODUCT_ROWS)
        for row in rows:

            if product_name in row.text:
                product_link = row.find_element(
                    By.CSS_SELECTOR,
                    "td strong a"
                )
                product_link.click()
                return

        raise AssertionError(
            f"Product not found: {product_name}"
        )