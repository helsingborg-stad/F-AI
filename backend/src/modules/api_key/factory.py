from pymongo.asynchronous.database import AsyncDatabase

from src.modules.api_key.MongoApiKeyService import MongoApiKeyService
from src.modules.api_key.protocols.IApiKeyService import IApiKeyService


class ApiKeyServiceFactory:
    def __init__(self, mongo_database: AsyncDatabase):
        self._mongo_database = mongo_database

    def get(self) -> IApiKeyService:
        return MongoApiKeyService(self._mongo_database)
