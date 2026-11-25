from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from support.seed import Seed


def test_admin_logs_in_and_lands_on_admin_home(page: Page, seed: Seed) -> None:
    admin = seed.user(admin=True)
    login_page = LoginPage(page)

    login_page.open()
    login_page.login(admin.email, admin.password)

    expect(page).to_have_url("/admin/home")
    expect(page.get_by_role("heading", name=f"Bem Vindo {admin.name}")).to_be_visible()


def test_wrong_password_shows_error_and_stores_no_token(page: Page, seed: Seed) -> None:
    customer = seed.user(admin=False)
    login_page = LoginPage(page)

    login_page.open()
    login_page.login(customer.email, f"{customer.password}-wrong")

    expect(login_page.error_alert).to_contain_text("Email e/ou senha inválidos")
    expect(page).to_have_url(LoginPage.URL)
    assert page.evaluate("localStorage.getItem('serverest/userToken')") is None
