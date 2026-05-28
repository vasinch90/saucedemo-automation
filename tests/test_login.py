"""
test_login.py — Test Cases สำหรับหน้า Login ของ SauceDemo
----------------------------------------------------------
ครอบคลุม 6 scenarios:
  1. Login ด้วย username/password ที่ถูกต้อง
  2. Login ด้วย password ผิด
  3. Login โดยไม่กรอก username
  4. Login โดยไม่กรอก password
  5. Login ด้วยบัญชีที่ถูกล็อก (locked_out_user)
  6. Login หลายบัญชีพร้อมกัน (parametrize)

วิธี run:
  pytest tests/test_login.py -v
  pytest tests/test_login.py -v --html=report.html   (ต้องติดตั้ง pytest-html)
"""

import pytest
from pages.login_page import LoginPage
from conftest import VALID_USER, VALID_PASSWORD, LOCKED_USER


class TestLogin:
    """รวม test cases ทั้งหมดของหน้า Login"""

    # ============================================================
    # POSITIVE TEST CASES — คาดว่า login สำเร็จ
    # ============================================================

    def test_valid_login(self, driver):
        """
        TC-LOGIN-01: Login ด้วย username/password ถูกต้อง
        Expected: เปลี่ยนหน้าไปที่ /inventory.html
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(VALID_USER, VALID_PASSWORD)

        assert login_page.is_login_successful(), (
            f"❌ Login ไม่สำเร็จ — URL ปัจจุบัน: {login_page.get_current_url()}"
        )

    def test_login_redirects_to_inventory(self, driver):
        """
        TC-LOGIN-02: หลัง login สำเร็จ URL ต้องมี /inventory.html
        Expected: current URL contains '/inventory.html'
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(VALID_USER, VALID_PASSWORD)

        current_url = login_page.get_current_url()
        assert "/inventory.html" in current_url, (
            f"❌ ควร redirect ไป inventory แต่ได้ URL: {current_url}"
        )

    # ============================================================
    # NEGATIVE TEST CASES — คาดว่า login ล้มเหลวพร้อม error
    # ============================================================

    def test_invalid_password(self, driver):
        """
        TC-LOGIN-03: Login ด้วย password ผิด
        Expected: เห็น error message, ยังอยู่หน้า login
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(VALID_USER, "wrong_password_123")

        assert login_page.is_error_visible(), "❌ ควรแสดง error message แต่ไม่พบ"
        assert login_page.is_on_login_page(), "❌ ควรยังอยู่หน้า login"

        error_text = login_page.get_error_message()
        assert "Username and password do not match" in error_text, (
            f"❌ Error message ไม่ถูกต้อง: {error_text}"
        )

    def test_empty_username(self, driver):
        """
        TC-LOGIN-04: กด Login โดยไม่กรอก username
        Expected: error แจ้งว่า Username is required
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("", VALID_PASSWORD)   # username ว่าง

        assert login_page.is_error_visible(), "❌ ควรแสดง error message"

        error_text = login_page.get_error_message()
        assert "Username is required" in error_text, (
            f"❌ Error message ไม่ถูกต้อง: {error_text}"
        )

    def test_empty_password(self, driver):
        """
        TC-LOGIN-05: กด Login โดยไม่กรอก password
        Expected: error แจ้งว่า Password is required
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(VALID_USER, "")   # password ว่าง

        assert login_page.is_error_visible(), "❌ ควรแสดง error message"

        error_text = login_page.get_error_message()
        assert "Password is required" in error_text, (
            f"❌ Error message ไม่ถูกต้อง: {error_text}"
        )

    def test_locked_out_user(self, driver):
        """
        TC-LOGIN-06: Login ด้วย locked_out_user
        Expected: error แจ้งว่าบัญชีถูกล็อก
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(LOCKED_USER, VALID_PASSWORD)

        assert login_page.is_error_visible(), "❌ ควรแสดง error สำหรับ locked user"

        error_text = login_page.get_error_message()
        assert "locked out" in error_text.lower(), (
            f"❌ Error message ไม่ถูกต้อง: {error_text}"
        )

    # ============================================================
    # PARAMETRIZE — ทดสอบหลาย input พร้อมกันในครั้งเดียว
    # ============================================================

    @pytest.mark.parametrize("username, password, expected_error", [
        ("",             "",               "Username is required"),
        ("wrong_user",   "secret_sauce",   "Username and password do not match"),
        ("standard_user","wrong_pass",     "Username and password do not match"),
        (LOCKED_USER,    VALID_PASSWORD,   "locked out"),
    ])
    def test_various_invalid_logins(self, driver, username, password, expected_error):
        """
        TC-LOGIN-07: ทดสอบ invalid login หลาย scenarios ด้วย parametrize
        pytest จะ run test นี้ 4 รอบ แต่ละรอบใช้ input ต่างกัน
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(username, password)

        assert login_page.is_error_visible(), (
            f"❌ ควรมี error สำหรับ user='{username}'"
        )
        assert expected_error.lower() in login_page.get_error_message().lower(), (
            f"❌ Error ไม่ตรง — ได้: '{login_page.get_error_message()}'"
        )
