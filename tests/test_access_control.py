from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.product_form_page import ProductFormPage
from pages.store_page import StorePage
from support.api_client import ServeRestClient
from support.seed import Seed
from support.session import OpenSession


def test_anonymous_visitor_is_redirected_to_login(page: Page) -> None:
    page.goto(StorePage.URL)

    expect(page).to_have_url(LoginPage.URL)
    expect(LoginPage(page).heading).to_be_visible()


def test_expired_session_cannot_register_product(
    open_session: OpenSession, seed: Seed, api: ServeRestClient
) -> None:
    page = open_session(seed.user(admin=True), valid_token=False)
    product = seed.unsaved_product()
    form = ProductFormPage(page)

    form.open()
    form.register(product)

    expect(form.error_alert).to_contain_text("Token de acesso ausente, inválido, expirado")
    expect(page).to_have_url(ProductFormPage.URL)
    assert api.find_products(product.name) == {}


def test_customer_cannot_register_product(
    customer_page: Page, seed: Seed, api: ServeRestClient
) -> None:
    product = seed.unsaved_product()
    form = ProductFormPage(customer_page)

    form.open()
    form.register(product)

    expect(form.error_alert).to_contain_text("Rota exclusiva para administradores")
    expect(customer_page).to_have_url(ProductFormPage.URL)
    assert api.find_products(product.name) == {}
