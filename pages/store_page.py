from playwright.sync_api import Locator, Page


class StorePage:
    URL = "/home"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.add_to_list_button = page.get_by_test_id("adicionarNaLista")

    def open(self) -> None:
        self.page.goto(self.URL)
        # The full catalogue arrives after render and overwrites a search fired before it.
        self.add_to_list_button.first.wait_for()

    def search(self, name: str) -> None:
        self.page.get_by_test_id("pesquisar").fill(name)
        self.page.get_by_test_id("botaoPesquisar").click()

    def product_title(self, name: str) -> Locator:
        return self.page.get_by_role("heading", name=name)
