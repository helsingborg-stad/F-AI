from pymongo.asynchronous.database import AsyncDatabase

from src.modules.settings.MongoSettingsService import MongoSettingsService
from src.modules.settings.protocols.ISettingsService import ISettingsService


class SettingsServiceFactory:
    def __init__(self, mongo_database: AsyncDatabase):
        self._mongo_database = mongo_database

    def get(self) -> ISettingsService:
        return MongoSettingsService(self._mongo_database)
