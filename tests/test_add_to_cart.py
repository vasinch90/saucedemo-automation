import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from conftest import VALID_USER, VALID_PASSWORD

class TestAddToCart:

    def setup_method(self):
        """
        pytest เรียก method นี้อัตโนมัติก่อนทุก test
        ใช้เตรียม Page Object ที่จะใช้ร่วมกันใน class
        """

        pass # driver จะมาจาก fixture ด้านล่าง

    def test_add_item_to_cart(self, logged_in_driver):
        """
        TC-CART-01: กด Add to cart → cart badge แสดงเลข 1
        ใช้ logged_in_driver จาก conftest.py (login มาให้แล้ว)
        """

        inventory = InventoryPage(logged_in_driver)

        #เช็คก่อนว่าตะกร้าว่างอยู่
        assert inventory.get_cart_count() == 0, "❌ ควรเริ่มต้นด้วย cart ว่าง"

        # กด Add to cart
        inventory.add_backpack_to_cart()

        # เช็คว่า badge แสดงเลข 1
        assert inventory.get_cart_count() == 1, "❌ Cart badge ควรแสดงเลข 1"

        # ✅ เพิ่มบรรทัดนี้ — ล้าง state ก่อนออกจาก test
        inventory.remove_backpack_from_cart()

    def test_remove_item_from_cart(self, logged_in_driver):
        """
        TC-CART-02: เพิ่มสินค้า → แล้วลบออก → badge หายไป
        """
        inventory = InventoryPage(logged_in_driver)

        inventory.add_backpack_to_cart()
        assert inventory.get_cart_count() == 1, "❌ ควรมี 1 ชิ้นก่อนลบ"

        inventory.remove_backpack_from_cart()
        assert inventory.get_cart_count() == 0, "❌ Cart ควรว่างหลังลบ"

    def test_inventory_has_six_items(self, logged_in_driver):
        """
        TC-CART-03: หน้า inventory ต้องแสดงสินค้า 6 ชิ้นเสมอ
        """
        inventory = InventoryPage(logged_in_driver)

        items = inventory.get_all_item_names()

        assert len(items) == 6, f"❌ ควรมี 6 ชิ้น แต่เจอ {len(items)} ชิ้น"
        assert "Sauce Labs Backpack" in items, "❌ ไม่เจอ Backpack ในรายการ"

    def setup_method(self, method):
        """pytest เรียกอัตโนมัติก่อนทุก test method"""
        print(f"\n▶ เริ่ม: {method.__name__}")

    def teardown_method(self, method):
        """pytest เรียกอัตโนมัติหลังทุก test method"""
        print(f"✓ จบ: {method.__name__}")