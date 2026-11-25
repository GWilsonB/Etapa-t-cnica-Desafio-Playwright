from playwright.sync_api import Page

from support.factories import Product


class ProductFormPage:
    URL = "/admin/cadastrarprodutos"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.error_alert = page.get_by_role("alert")

    def open(self) -> None:
        self.page.goto(self.URL)

    def register(self, product: Product) -> None:
        self.page.get_by_test_id("nome").fill(product.name)
        self.page.get_by_test_id("preco").fill(str(product.price))
        self.page.get_by_test_id("descricao").fill(product.description)
        self.page.get_by_test_id("quantity").fill(str(product.quantity))
        # "cadastar" is how the application itself spells this data-testid.
        self.page.get_by_test_id("cadastarProdutos").click()
