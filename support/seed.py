from support.api_client import ServeRestClient
from support.factories import Product, User, build_product, build_user


class Seed:
    """Creates test data through the API and removes everything it tracked."""

    def __init__(self, api: ServeRestClient) -> None:
        self._api = api
        self._user_ids: list[str] = []
        self._product_names: list[str] = []
        self._admin_token: str | None = None

    def user(self, *, admin: bool) -> User:
        user = build_user(admin=admin)
        self._user_ids.append(self._api.create_user(user))
        return user

    def product(self) -> Product:
        product = self.unsaved_product()
        self._api.create_product(product, self._token())
        return product

    def unsaved_product(self) -> Product:
        """A product the test will try to create through the UI; tracked up front for cleanup."""
        product = build_product()
        self._product_names.append(product.name)
        return product

    def cleanup(self) -> None:
        # Products go first: deleting them needs the token of an admin that still exists.
        for name in self._product_names:
            for product_id in self._api.find_products(name):
                self._api.delete_product(product_id, self._token())
        for user_id in self._user_ids:
            self._api.delete_user(user_id)

    def _token(self) -> str:
        if self._admin_token is None:
            self._admin_token = self._api.login(self.user(admin=True))
        return self._admin_token
