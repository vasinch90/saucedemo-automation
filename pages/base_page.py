"""
base_page.py — Base class สำหรับทุก Page Object
-------------------------------------------------
รวม method พื้นฐานที่ทุกหน้าใช้ร่วมกัน เช่น click, type, get_text
ทำให้ login_page.py, inventory_page.py ฯลฯ ไม่ต้องเขียนซ้ำ
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    """Page Object base class — Page ทุกหน้าให้ inherit จากนี้"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=10)   # Explicit wait สูงสุด 10 วิ

    # --------------------------------------------------------
    # Navigation
    # --------------------------------------------------------

    def open(self, url: str):
        """เปิด URL"""
        self.driver.get(url)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    # --------------------------------------------------------
    # Element interactions (รอ element ก่อนทุกครั้ง)
    # --------------------------------------------------------

    def find(self, locator: tuple):
        """รอจนเห็น element แล้วคืนกลับ"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator: tuple):
        """รอให้ clickable แล้วคลิก"""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator: tuple, text: str):
        """ล้างค่าเดิมแล้วพิมพ์ข้อความ"""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        """คืนค่า text ของ element"""
        return self.find(locator).text

    def is_visible(self, locator: tuple) -> bool:
        """ตรวจว่า element แสดงอยู่ไหม (ไม่ throw error ถ้าไม่เจอ)"""
        try:
            return self.find(locator).is_displayed()
        except Exception:
            return False
