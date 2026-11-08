from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import LOGIN_URL

class LoginPage(BasePage):

    EMAIL_FIELD = (By.NAME, "email")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    def open_login_page(self):
        self.open(LOGIN_URL)

    def login(self, email, password):
        self.enter_text(self.EMAIL_FIELD, email)
        self.enter_text(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)