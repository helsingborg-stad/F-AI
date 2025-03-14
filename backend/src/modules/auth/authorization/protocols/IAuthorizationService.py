from typing import Protocol

from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity
from src.modules.auth.authorization.models.GrantedScopes import GrantedScopes


class IAuthorizationService(Protocol):
    async def has_scopes(self, identity: AuthenticatedIdentity, scopes: list[str]) -> bool:
        ...

    async def get_scopes(self, identity: AuthenticatedIdentity) -> GrantedScopes:
        ...
