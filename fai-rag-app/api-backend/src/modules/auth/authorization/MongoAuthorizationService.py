from pymongo.asynchronous.database import AsyncDatabase

from src.modules.api_key.protocols.IApiKeyService import IApiKeyService
from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity
from src.modules.auth.authorization.protocols.IAuthorizationService import IAuthorizationService


class MongoAuthorizationService(IAuthorizationService):
    def __init__(self, database: AsyncDatabase, api_key_service: IApiKeyService):
        self._database = database
        self._api_key_service = api_key_service

    async def has_scopes(self, identity: AuthenticatedIdentity, scopes: list[str]) -> bool:
        # TODO: check user bearer token

        api_key = await self._api_key_service.find_by_revoke_id(identity.uid)

        if api_key is not None:
            return all(scope in api_key.scopes for scope in scopes)

        return False
