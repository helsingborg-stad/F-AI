from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity
from src.modules.auth.authorization.protocols.IAuthorizationService import IAuthorizationService


class AlwaysAuthorizedAuthorizationService(IAuthorizationService):
    async def has_scopes(self, identity: AuthenticatedIdentity, scopes: list[str]) -> bool:
        return True
