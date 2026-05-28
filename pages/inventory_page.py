from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InventoryPage(BasePage):
    URL = "https://www.saucedemo.com/inventory.html"

    # Locators
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    CART_ICON = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "[data-test='add-to-cart-sauce-labs-backpack']")
    REMOVE_BTN = (By.CSS_SELECTOR, "[data-test='remove-sauce-labs-backpack']")
    SORT_DROPDOWN  = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    ITEM_PRICES    = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")

    def get_cart_count(self) -> int:
        """คืนจำนวนสินค้าที่อยู่ใน cart (ถ้าไม่มี badge ให้ถือว่าเป็น 0)"""
        if self.is_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def add_backpack_to_cart(self):
        """คลิกปุ่ม Add to cart ของสินค้าชื่อ 'Sauce Labs Backpack'"""
        self.click(self.ADD_TO_CART_BTN)

    def remove_backpack_from_cart(self):
        """คลิกปุ่ม Remove ของสินค้าชื่อ 'Sauce Labs Backpack'"""
        self.click(self.REMOVE_BTN)

    def get_all_item_names(self) -> list:
        """คืน list ของชื่อสินค้าทั้งหมดในหน้า inventory"""
        elements = self.driver.find_elements(*self.ITEM_NAMES)
        return [el.text for el in elements]

    def go_to_cart(self):
        """คลิกปุ่ม ตะกร้า เพื่อไปหน้า cart"""
        self.click(self.CART_BADGE)

    def sort_by(self, value: str):
        """
        เลือก sort option ด้วย value
        value: 'az', 'za', 'lohi', 'hilo'
        """
        dropdown = self.find(self.SORT_DROPDOWN)
        Select(dropdown).select_by_value(value)

    def get_all_prices(self) -> list:
        """คืน list ราคาสินค้าทุกชิ้น เป็น float"""
        elements = self.driver.find_elements(*self.ITEM_PRICES)
        # "$7.99" → 7.99  ตัด $ ออกแล้วแปลงเป็นตัวเลข
        return [float(el.text.replace("$", "")) for el in elements]