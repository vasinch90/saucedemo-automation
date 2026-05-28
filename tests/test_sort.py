from pages.inventory_page import InventoryPage


class TestSort:

    def test_sort_name_a_to_z(self, logged_in_driver):
        """
        TC-SORT-01: Sort Name A→Z
        ชื่อสินค้าที่ได้ต้องเรียงเหมือนกับที่ sort() เรียงให้
        """
        inventory = InventoryPage(logged_in_driver)
        inventory.sort_by("az")

        names = inventory.get_all_item_names()
        assert names == sorted(names), (
            f"❌ ชื่อสินค้าไม่ได้เรียง A→Z\nได้: {names}"
        )

    def test_sort_name_z_to_a(self, logged_in_driver):
        """
        TC-SORT-02: Sort Name Z→A
        """
        inventory = InventoryPage(logged_in_driver)
        inventory.sort_by("za")

        names = inventory.get_all_item_names()
        assert names == sorted(names, reverse=True), (
            f"❌ ชื่อสินค้าไม่ได้เรียง Z→A\nได้: {names}"
        )

    def test_sort_price_low_to_high(self, logged_in_driver):
        """
        TC-SORT-03: Sort Price Low→High
        ราคาแต่ละชิ้นต้องไม่น้อยกว่าชิ้นก่อนหน้า
        """
        inventory = InventoryPage(logged_in_driver)
        inventory.sort_by("lohi")

        prices = inventory.get_all_prices()
        assert prices == sorted(prices), (
            f"❌ ราคาไม่ได้เรียงจากน้อยไปมาก\nได้: {prices}"
        )

    def test_sort_price_high_to_low(self, logged_in_driver):
        """
        TC-SORT-04: Sort Price High→Low
        """
        inventory = InventoryPage(logged_in_driver)
        inventory.sort_by("hilo")

        prices = inventory.get_all_prices()
        assert prices == sorted(prices, reverse=True), (
            f"❌ ราคาไม่ได้เรียงจากมากไปน้อย\nได้: {prices}"
        )