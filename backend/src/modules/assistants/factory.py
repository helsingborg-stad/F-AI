from pymongo.asynchronous.database import AsyncDatabase

from src.modules.assistants.MongoAssistantService import MongoAssistantService
from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.resources.protocols.IResourceService import IResourceService


class AssistantServiceFactory:
    def __init__(self, mongo_database: AsyncDatabase, resource_service: IResourceService):
        self._mongo_database = mongo_database
        self._resource_service = resource_service

    def get(self) -> IAssistantService:
        return MongoAssistantService(database=self._mongo_database, resource_service=self._resource_service)
