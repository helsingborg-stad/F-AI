from typing import Protocol

from src.modules.authentication.models import AuthenticatedIdentity


class IAuthenticationService(Protocol):
    async def authenticate(self, payload: str) -> AuthenticatedIdentity | None:
        ...
