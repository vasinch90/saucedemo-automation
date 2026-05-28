"""
conftest.py — pytest fixtures สำหรับ SauceDemo Automation Project
-----------------------------------------------------------------
ไฟล์นี้จะถูก pytest โหลดอัตโนมัติก่อน run test ทุกครั้ง
Fixture ที่กำหนดที่นี่สามารถใช้ใน test file ทุกไฟล์ได้เลย
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# ============================================================
# Constants — ข้อมูลกลางของโปรเจกต์
# ============================================================

BASE_URL = "https://www.saucedemo.com"

# Test accounts ที่ SauceDemo เตรียมไว้ให้
VALID_USER      = "standard_user"
LOCKED_USER     = "locked_out_user"   # บัญชีที่ถูกล็อก (ใช้ทดสอบ error)
PROBLEM_USER    = "problem_user"      # บัญชีที่มี bug จงใจ
VALID_PASSWORD  = "secret_sauce"


# ============================================================
# Fixture: driver
# scope="function" = สร้าง browser ใหม่ทุก test case (แนะนำ)
# ============================================================

@pytest.fixture(scope="class")
def driver():
    """
    เปิด Chrome browser ก่อน test และปิดหลัง test เสมอ
    ใช้ headless=False เพื่อดู browser ระหว่างพัฒนา
    เปลี่ยนเป็น headless=True เมื่อ run บน CI/CD
    """
    options = Options()

    # --- uncommnet บรรทัดด้านล่างเมื่อ run บน CI/CD (GitHub Actions) ---
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")

    options.add_argument("--window-size=1280,800")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-features=PasswordLeakDetection")
    options.add_argument("--disable-features=AutofillServerCommunication")
    options.add_argument("--incognito")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,       # ปิด password manager
        "profile.password_manager_enabled": False, # ปิด popup บันทึก password
        "profile.default_content_setting_values.notifications": 2  # ปิด notification popup
    })

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(5)          # รอ element สูงสุด 5 วินาที

    yield browser                        # ส่ง driver ให้ test ใช้งาน

    browser.quit()                       # ปิด browser หลัง test จบเสมอ


# ============================================================
# Fixture: logged_in_driver  (shortcut สำหรับ test ที่ต้อง login ก่อน)
# ============================================================

@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """
    เปิด browser + login สำเร็จแล้ว → ส่งให้ test ที่ต้องการหน้า inventory
    ใช้สำหรับ test_cart.py, test_checkout.py ฯลฯ
    """
    from pages.login_page import LoginPage

    login = LoginPage(driver)
    login.open()
    login.login(VALID_USER, VALID_PASSWORD)

    yield driver
