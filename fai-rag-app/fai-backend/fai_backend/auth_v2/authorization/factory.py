from fai_backend.auth_v2.authorization.impl.repo import RepoAuthorizationProvider
from fai_backend.auth_v2.authorization.models import IAuthorizationProvider


class AuthorizationFactory:
    @staticmethod
    async def get() -> IAuthorizationProvider:
        return RepoAuthorizationProvider()
