import time
from typing import Any

from playwright.sync_api import APIRequestContext, APIResponse

from support.factories import Product, User


class ServeRestClient:
    def __init__(self, request: APIRequestContext) -> None:
        self._request = request

    def create_user(self, user: User) -> str:
        payload = {
            "nome": user.name,
            "email": user.email,
            "password": user.password,
            "administrador": str(user.is_admin).lower(),
        }
        user_id: str = self._send("POST", "/usuarios", 201, data=payload)["_id"]
        return user_id

    def delete_user(self, user_id: str) -> None:
        self._send("DELETE", f"/usuarios/{user_id}", 200)

    def login(self, user: User) -> str:
        credentials = {"email": user.email, "password": user.password}
        token: str = self._send("POST", "/login", 200, data=credentials)["authorization"]
        return token

    def create_product(self, product: Product, token: str) -> str:
        payload = {
            "nome": product.name,
            "preco": product.price,
            "descricao": product.description,
            "quantidade": product.quantity,
        }
        headers = {"Authorization": token}
        product_id: str = self._send("POST", "/produtos", 201, data=payload, headers=headers)["_id"]
        return product_id

    def find_products(self, name: str) -> dict[str, Product]:
        body = self._send("GET", "/produtos", 200, params={"nome": name})
        return {
            item["_id"]: Product(
                name=item["nome"],
                price=item["preco"],
                description=item["descricao"],
                quantity=item["quantidade"],
            )
            for item in body["produtos"]
        }

    def delete_product(self, product_id: str, token: str) -> None:
        self._send("DELETE", f"/produtos/{product_id}", 200, headers={"Authorization": token})

    def _send(self, method: str, path: str, expected_status: int, **options: Any) -> dict[str, Any]:
        response = self._fetch(method, path, **options)
        if response.status == 429:
            # The public server is rate limited and says how long to wait.
            time.sleep(float(response.headers.get("retry-after", "1")))
            response = self._fetch(method, path, **options)
        if response.status != expected_status:
            raise AssertionError(
                f"{method} {path} returned {response.status}, expected {expected_status}: "
                f"{response.text()}"
            )
        body: dict[str, Any] = response.json()
        return body

    def _fetch(self, method: str, path: str, **options: Any) -> APIResponse:
        return self._request.fetch(path, method=method, **options)
