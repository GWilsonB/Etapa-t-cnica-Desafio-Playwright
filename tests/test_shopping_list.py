import pytest
from playwright.sync_api import Page, expect

from pages.shopping_list_page import ShoppingListPage
from pages.store_page import StorePage
from support.factories import Product
from support.seed import Seed


def add_to_shopping_list(page: Page, product: Product) -> ShoppingListPage:
    store = StorePage(page)
    store.open()
    store.search(product.name)
    expect(store.add_to_list_button).to_have_count(1)
    expect(store.product_title(product.name)).to_be_visible()
    store.add_to_list_button.click()
    expect(page).to_have_url(ShoppingListPage.URL)
    return ShoppingListPage(page)


def test_customer_adds_product_and_total_follows_quantity(customer_page: Page, seed: Seed) -> None:
    product = seed.product()

    shopping_list = add_to_shopping_list(customer_page, product)

    expect(shopping_list.product_name).to_contain_text(product.name)
    expect(shopping_list.quantity).to_have_text("Total: 1")
    expect(shopping_list.line_total).to_have_text(f"Preço R${product.price}")

    shopping_list.increase_button.click()

    expect(shopping_list.quantity).to_have_text("Total: 2")
    expect(shopping_list.line_total).to_have_text(f"Preço R${product.price * 2}")


@pytest.mark.xfail(
    strict=True,
    reason="Front bug: '-' at quantity 1 keeps the product in the list "
    "(Cart.deleteItem filters by `id`, but items are stored with `_id`).",
)
def test_decreasing_the_last_unit_removes_the_product(customer_page: Page, seed: Seed) -> None:
    shopping_list = add_to_shopping_list(customer_page, seed.product())

    shopping_list.decrease_button.click()

    # The list re-renders on the click itself, so a short wait is enough to tell.
    expect(shopping_list.empty_message).to_be_visible(timeout=2_000)
