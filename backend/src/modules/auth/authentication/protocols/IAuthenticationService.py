from typing import Protocol

from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity


class IAuthenticationService(Protocol):
    async def authenticate(self, payload: str) -> AuthenticatedIdentity | None:
        ...
