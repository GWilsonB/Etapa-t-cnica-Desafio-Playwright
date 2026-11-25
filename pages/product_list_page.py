from playwright.sync_api import Locator, Page

from support.factories import Product


class ProductListPage:
    URL = "/admin/listarprodutos"

    def __init__(self, page: Page) -> None:
        self.page = page

    def row(self, name: str) -> Locator:
        return self.page.get_by_role("row").filter(has_text=name)

    def read(self, name: str) -> Product:
        cells = self.row(name).get_by_role("cell").all_inner_texts()
        return Product(
            name=cells[0],
            price=int(cells[1]),
            description=cells[2],
            quantity=int(cells[3]),
        )
