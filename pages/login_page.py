"""
login_page.py — Page Object สำหรับหน้า Login ของ SauceDemo
-----------------------------------------------------------
URL: https://www.saucedemo.com

โครงสร้าง Page Object Model (POM):
  1. LOCATORS  — เก็บตำแหน่ง element ทั้งหมดไว้ที่เดียว
  2. ACTIONS   — method ที่ทำ action บนหน้านี้
  3. ASSERTIONS helper — method ช่วยตรวจสอบผลลัพธ์

ข้อดีของ POM: ถ้า element เปลี่ยน เช่น id เปลี่ยน
แก้แค่ LOCATORS ที่นี่ที่เดียว → test ทุกไฟล์ทำงานต่อได้
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):

    # ============================================================
    # LOCATORS — ตำแหน่ง element บนหน้า Login
    # ============================================================

    URL = "https://www.saucedemo.com"

    USERNAME_INPUT  = (By.ID, "user-name")
    PASSWORD_INPUT  = (By.ID, "password")
    LOGIN_BUTTON    = (By.ID, "login-button")
    ERROR_MESSAGE   = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_ICON      = (By.CSS_SELECTOR, ".error_icon")
    LOGIN_LOGO      = (By.CLASS_NAME, "login_logo")

    # ============================================================
    # ACTIONS
    # ============================================================

    def open(self):
        """เปิดหน้า Login"""
        super().open(self.URL)

    def enter_username(self, username: str):
        """พิมพ์ username"""
        self.type(self.USERNAME_INPUT, username)

    def enter_password(self, password: str):
        """พิมพ์ password"""
        self.type(self.PASSWORD_INPUT, password)

    def click_login(self):
        """กดปุ่ม Login"""
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        """
        Shortcut: พิมพ์ username + password + กด Login ในครั้งเดียว
        ใช้ใน conftest.py และ test ที่ต้อง login ก่อนทำอย่างอื่น
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ============================================================
    # ASSERTION HELPERS — ช่วย test ตรวจสอบผลลัพธ์
    # ============================================================

    def get_error_message(self) -> str:
        """คืนข้อความ error (ถ้ามี)"""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_visible(self) -> bool:
        """ตรวจว่ามี error message แสดงอยู่ไหม"""
        return self.is_visible(self.ERROR_MESSAGE)

    def is_on_login_page(self) -> bool:
        """ตรวจว่ายังอยู่หน้า login (logo มองเห็น)"""
        return self.is_visible(self.LOGIN_LOGO)

    def is_login_successful(self) -> bool:
        """ตรวจว่า login สำเร็จ → URL เปลี่ยนไปหน้า inventory"""
        return "/inventory.html" in self.get_current_url()
