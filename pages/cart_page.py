from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):

    # Locators
    CHECKOUT_BTN   = (By.CSS_SELECTOR, "[data-test='checkout']")
    ITEM_NAMES     = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")

    def click_checkout(self):
        self.click(self.CHECKOUT_BTN)

    def get_item_names(self) -> list:
        elements = self.driver.find_elements(*self.ITEM_NAMES)
        return [el.text for el in elements]

    def is_item_in_cart(self, item_name: str) -> bool:
        return item_name in self.get_item_names()