from src.modules.api_key.protocols.IApiKeyService import IApiKeyService
from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity
from src.modules.auth.authentication.protocols.IAuthenticationService import IAuthenticationService


class ApiKeyAuthenticationService(IAuthenticationService):
    def __init__(self, api_key_service: IApiKeyService):
        self._api_key_service = api_key_service

    async def authenticate(self, payload: str) -> AuthenticatedIdentity | None:
        key = await self._api_key_service.find_by_key(payload)

        if key is None:
            return None

        return AuthenticatedIdentity(
            principal_type='application',
            uid=key.revoke_id,
        )
