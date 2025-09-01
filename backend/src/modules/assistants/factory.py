from pymongo.asynchronous.database import AsyncDatabase

from src.modules.assistants.MongoAssistantService import MongoAssistantService
from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.models.protocols.IModelService import IModelService
from src.modules.resources.protocols.IResourceService import IResourceService


class AssistantServiceFactory:
    def __init__(self, mongo_database: AsyncDatabase, resource_service: IResourceService, model_service: IModelService):
        self._mongo_database = mongo_database
        self._resource_service = resource_service
        self._model_service = model_service

    def get(self) -> IAssistantService:
        return MongoAssistantService(
            database=self._mongo_database, 
            resource_service=self._resource_service,
            model_service=self._model_service
        )
