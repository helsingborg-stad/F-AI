from pymongo.asynchronous.database import AsyncDatabase

from src.modules.assistants.MongoAssistantService import MongoAssistantService
from src.modules.assistants.protocols.IAssistantService import IAssistantService


class AssistantServiceFactory:
    def __init__(self, mongo_database: AsyncDatabase):
        self._mongo_database = mongo_database

    def get(self) -> IAssistantService:
        return MongoAssistantService(self._mongo_database)
