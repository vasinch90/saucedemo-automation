from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestCheckout:

    def test_full_checkout_flow(self, logged_in_driver):
        """
        TC-CHECKOUT-01: Happy path — checkout จนจบสำเร็จ
        Flow: inventory → cart → step1 → step2 → complete
        """
        # Step 1: เพิ่มสินค้า
        inventory = InventoryPage(logged_in_driver)
        inventory.add_backpack_to_cart()
        inventory.go_to_cart()

        # Step 2: เช็คสินค้าในตะกร้า แล้วไป checkout
        cart = CartPage(logged_in_driver)
        assert cart.is_item_in_cart("Sauce Labs Backpack"), "❌ ไม่เจอสินค้าในตะกร้า"
        cart.click_checkout()

        # Step 3: กรอกข้อมูล
        checkout = CheckoutPage(logged_in_driver)
        checkout.fill_info("Benz", "Test", "10400")
        checkout.click_continue()

        # Step 4: ยืนยันคำสั่งซื้อ
        checkout.click_finish()

        # Step 5: ตรวจ complete page
        assert checkout.is_order_complete(), (
            f"❌ ไม่เจอ 'Thank you' — เห็น: '{checkout.get_complete_header()}'"
        )

    def test_checkout_missing_firstname(self, logged_in_driver):
        """
        TC-CHECKOUT-02: ไม่กรอก First Name → ต้องเห็น error
        """
        inventory = InventoryPage(logged_in_driver)
        inventory.add_backpack_to_cart()
        inventory.go_to_cart()

        CartPage(logged_in_driver).click_checkout()

        checkout = CheckoutPage(logged_in_driver)
        checkout.fill_info("", "Test", "10400")   # first name ว่าง
        checkout.click_continue()

        assert checkout.is_error_visible(), "❌ ควรแสดง error"
        assert "First Name is required" in checkout.get_error_message(), (
            f"❌ Error ไม่ถูกต้อง: {checkout.get_error_message()}"
        )

        # ล้าง state — กลับไปลบสินค้าออกจาก cart
        logged_in_driver.back()
        logged_in_driver.back()
        InventoryPage(logged_in_driver).remove_backpack_from_cart()

    def test_checkout_missing_lastname(self, logged_in_driver):
        """
        TC-CHECKOUT-03: ไม่กรอก Last Name → ต้องเห็น error
        """
        inventory = InventoryPage(logged_in_driver)
        inventory.add_backpack_to_cart()
        inventory.go_to_cart()

        CartPage(logged_in_driver).click_checkout()

        checkout = CheckoutPage(logged_in_driver)
        checkout.fill_info("Benz", "", "10400")   # last name ว่าง
        checkout.click_continue()

        assert checkout.is_error_visible(), "❌ ควรแสดง error"
        assert "Last Name is required" in checkout.get_error_message(), (
            f"❌ Error ไม่ถูกต้อง: {checkout.get_error_message()}"
        )

        logged_in_driver.back()
        logged_in_driver.back()
        InventoryPage(logged_in_driver).remove_backpack_from_cart()