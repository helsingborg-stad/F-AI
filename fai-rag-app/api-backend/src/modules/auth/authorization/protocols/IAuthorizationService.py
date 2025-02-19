from typing import Protocol

from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity


class IAuthorizationService(Protocol):
    async def has_scopes(self, identity: AuthenticatedIdentity, scopes: list[str]) -> bool:
        ...
