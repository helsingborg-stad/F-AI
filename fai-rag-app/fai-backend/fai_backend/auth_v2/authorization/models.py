from typing import Protocol

from fai_backend.auth_v2.authentication.models import AuthenticatedIdentity


class IAuthorizationProvider(Protocol):
    async def has_scopes(self, identity: AuthenticatedIdentity, scopes: list[str]) -> bool:
        ...
