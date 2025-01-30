from fai_backend.auth_v2.api_key.dependencies import get_api_key_service
from fai_backend.auth_v2.authentication.models import AuthenticatedIdentity, AuthenticationType
from fai_backend.auth_v2.authorization.models import IAuthorizationProvider
from fai_backend.repositories import users_repo


class RepoAuthorizationProvider(IAuthorizationProvider):
    async def has_scopes(self, identity: AuthenticatedIdentity, scopes: list[str]) -> bool:
        user = await users_repo.get_user_by_email(identity.uid)

        if user is not None:
            permissions = user.projects[0].permissions
            return all(key in permissions and permissions[key] is True for key in scopes)

        api_key_service = await get_api_key_service()
        api_key = await api_key_service.find_by_revoke_id(identity.uid)

        if api_key is not None:
            return all(scope in api_key.scopes for scope in scopes)

        return False
