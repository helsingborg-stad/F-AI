from fai_backend.auth_v2.api_key.dependencies import get_api_key_service
from fai_backend.auth_v2.authentication.models import AuthenticatedIdentity, IAuthenticationProvider, AuthenticationType


class ApiKeyProvider(IAuthenticationProvider):
    async def validate(self, data: str | None) -> AuthenticatedIdentity | None:
        service = await get_api_key_service()
        key = await service.find_by_key(data)

        if not key:
            return None

        return AuthenticatedIdentity(
            uid=key.revoke_id
        )
