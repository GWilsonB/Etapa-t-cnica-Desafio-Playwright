from playwright.sync_api import Page


class ShoppingListPage:
    URL = "/minhaListaDeProdutos"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.product_name = page.get_by_test_id("shopping-cart-product-name")
        self.quantity = page.get_by_test_id("shopping-cart-product-quantity")
        self.line_total = page.get_by_text("Preço R$")
        self.increase_button = page.get_by_test_id("product-increase-quantity")
        self.decrease_button = page.get_by_test_id("product-decrease-quantity")
        self.empty_message = page.get_by_test_id("shopping-cart-empty-message")
