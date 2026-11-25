from collections.abc import Iterator

import pytest
from playwright.sync_api import Page, Playwright, expect
from pytest_playwright.pytest_playwright import CreateContextCallback

from support import config
from support.api_client import ServeRestClient
from support.factories import User
from support.seed import Seed
from support.session import INVALID_TOKEN, OpenSession, storage_state

# The target is a shared public environment; the default 5 s is tight under load.
expect.set_options(timeout=10_000)


@pytest.fixture(scope="session")
def base_url() -> str:
    return config.BASE_URL


@pytest.fixture(scope="session")
def api(playwright: Playwright) -> Iterator[ServeRestClient]:
    request = playwright.request.new_context(base_url=config.API_URL)
    yield ServeRestClient(request)
    request.dispose()


@pytest.fixture
def seed(api: ServeRestClient) -> Iterator[Seed]:
    seed = Seed(api)
    yield seed
    seed.cleanup()


@pytest.fixture
def open_session(new_context: CreateContextCallback, api: ServeRestClient) -> OpenSession:
    def open_session(user: User, *, valid_token: bool = True) -> Page:
        token = api.login(user) if valid_token else INVALID_TOKEN
        return new_context(storage_state=storage_state(user, token)).new_page()

    return open_session


@pytest.fixture
def admin_page(open_session: OpenSession, seed: Seed) -> Page:
    return open_session(seed.user(admin=True))


@pytest.fixture
def customer_page(open_session: OpenSession, seed: Seed) -> Page:
    return open_session(seed.user(admin=False))
