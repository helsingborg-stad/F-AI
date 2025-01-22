from fai_backend.auth_v2.authentication.models import AuthenticatedIdentity, AuthenticationType
from fai_backend.auth_v2.authorization.models import IAuthorizationProvider


class RepoAuthorizationProvider(IAuthorizationProvider):
    async def has_scopes(self, identity: AuthenticatedIdentity, scopes: list[str]) -> bool:
        # TODO
        return True
