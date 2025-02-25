import os

from pymongo.asynchronous.database import AsyncDatabase

from src.modules.api_key.protocols.IApiKeyService import IApiKeyService
from src.modules.auth.authorization.AlwaysAuthorizedAuthorizationService import AlwaysAuthorizedAuthorizationService
from src.modules.auth.authorization.MongoAuthorizationService import MongoAuthorizationService
from src.modules.auth.authorization.protocols.IAuthorizationService import IAuthorizationService


class AuthorizationServiceFactory:
    def __init__(self, mongo_database: AsyncDatabase, api_key_service: IApiKeyService):
        self._mongo_database = mongo_database
        self._api_key_service = api_key_service

    def get(self) -> IAuthorizationService:
        if os.environ['DISABLE_AUTH'] == '1':
            return AlwaysAuthorizedAuthorizationService()
        return MongoAuthorizationService(self._mongo_database, self._api_key_service)
