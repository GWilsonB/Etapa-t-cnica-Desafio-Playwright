from dataclasses import dataclass
from uuid import uuid4

from faker import Faker

fake = Faker("pt_BR")


@dataclass(frozen=True)
class User:
    name: str
    email: str
    password: str
    is_admin: bool


@dataclass(frozen=True)
class Product:
    name: str
    price: int
    description: str
    quantity: int


def _unique() -> str:
    return uuid4().hex[:10]


def build_user(*, admin: bool) -> User:
    return User(
        name=fake.name(),
        email=f"qa.{_unique()}@example.com",
        password=fake.password(length=12),
        is_admin=admin,
    )


def build_product() -> Product:
    return Product(
        name=f"Produto QA {_unique()}",
        price=fake.random_int(min=10, max=900),
        description="Produto criado por teste automatizado",
        quantity=fake.random_int(min=5, max=50),
    )
