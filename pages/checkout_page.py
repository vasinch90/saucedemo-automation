from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):

    # Locators — Step 1 (กรอกข้อมูล)
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "[data-test='firstName']")
    LAST_NAME_INPUT  = (By.CSS_SELECTOR, "[data-test='lastName']")
    POSTAL_CODE_INPUT= (By.CSS_SELECTOR, "[data-test='postalCode']")
    CONTINUE_BTN     = (By.CSS_SELECTOR, "[data-test='continue']")
    ERROR_MESSAGE    = (By.CSS_SELECTOR, "[data-test='error']")

    # Locators — Step 2 (สรุปคำสั่งซื้อ)
    FINISH_BTN       = (By.CSS_SELECTOR, "[data-test='finish']")

    # Locators — Complete
    COMPLETE_HEADER  = (By.CSS_SELECTOR, "[data-test='complete-header']")

    # Actions — Step 1
    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        """กรอกข้อมูลส่วนตัวครบทุกช่อง"""
        self.type(self.FIRST_NAME_INPUT, first_name)
        self.type(self.LAST_NAME_INPUT, last_name)
        self.type(self.POSTAL_CODE_INPUT, postal_code)

    def click_continue(self):
        self.click(self.CONTINUE_BTN)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_visible(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE)

    # Actions — Step 2
    def click_finish(self):
        self.click(self.FINISH_BTN)

    # Assertion — Complete
    def get_complete_header(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)

    def is_order_complete(self) -> bool:
        return "Thank you" in self.get_complete_header()