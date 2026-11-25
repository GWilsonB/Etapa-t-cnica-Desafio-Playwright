from typing import Protocol

from playwright.sync_api import Page, StorageState

from support import config
from support.factories import User

# The API answers the same 401 for a missing, malformed or expired token,
# so an invalid token stands in for a session that expired after 10 minutes.
INVALID_TOKEN = "Bearer expired.session.token"


class OpenSession(Protocol):
    def __call__(self, user: User, *, valid_token: bool = True) -> Page: ...


def storage_state(user: User, token: str) -> StorageState:
    """Mirrors what the front stores in localStorage after a successful login."""
    items = {"serverest/userEmail": user.email, "serverest/userToken": token}
    if user.is_admin:
        items["serverest/userNome"] = user.name
    return {
        "cookies": [],
        "origins": [
            {
                "origin": config.BASE_URL,
                "localStorage": [{"name": name, "value": value} for name, value in items.items()],
            }
        ],
    }
