from playwright.sync_api import Page, expect

from pages.product_form_page import ProductFormPage
from pages.product_list_page import ProductListPage
from support.api_client import ServeRestClient
from support.seed import Seed


def test_admin_registers_product(admin_page: Page, seed: Seed, api: ServeRestClient) -> None:
    product = seed.unsaved_product()
    form = ProductFormPage(admin_page)
    product_list = ProductListPage(admin_page)

    form.open()
    form.register(product)

    expect(admin_page).to_have_url(ProductListPage.URL)
    expect(product_list.row(product.name)).to_be_visible()
    assert product_list.read(product.name) == product
    assert list(api.find_products(product.name).values()) == [product]


def test_duplicate_product_name_is_rejected(
    admin_page: Page, seed: Seed, api: ServeRestClient
) -> None:
    existing = seed.product()
    form = ProductFormPage(admin_page)

    form.open()
    form.register(existing)

    expect(form.error_alert).to_contain_text("Já existe produto com esse nome")
    expect(admin_page).to_have_url(ProductFormPage.URL)
    assert list(api.find_products(existing.name).values()) == [existing]
