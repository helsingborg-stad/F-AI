from pymongo.asynchronous.database import AsyncDatabase

from src.modules.groups.MongoGroupService import MongoGroupService
from src.modules.groups.protocols.IGroupService import IGroupService


class GroupServiceFactory:
    def __init__(self, mongo_database: AsyncDatabase):
        self._mongo_database = mongo_database

    def get(self) -> IGroupService:
        return MongoGroupService(database=self._mongo_database)
