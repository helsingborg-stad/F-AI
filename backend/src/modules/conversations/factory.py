from pymongo.asynchronous.database import AsyncDatabase

from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.conversations.MongoConversationService import MongoConversationService
from src.modules.conversations.protocols.IConversationService import IConversationService


class ConversationServiceFactory:
    def __init__(self, mongo_database: AsyncDatabase, assistant_service: IAssistantService):
        self._mongo_database = mongo_database
        self._assistant_service = assistant_service

    def get(self) -> IConversationService:
        return MongoConversationService(database=self._mongo_database, assistant_service=self._assistant_service)
