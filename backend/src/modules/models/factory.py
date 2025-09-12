from pymongo.asynchronous.database import AsyncDatabase

from src.modules.models.MongoModelService import MongoModelService
from src.modules.models.protocols.IModelService import IModelService


class ModelServiceFactory:
    def __init__(self, mongo_database: AsyncDatabase):
        self._mongo_database = mongo_database

    def get(self) -> IModelService:
        return MongoModelService(database=self._mongo_database)