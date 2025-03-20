from pymongo.asynchronous.database import AsyncDatabase

from src.modules.conversations.MongoConversationService import MongoConversationService
from src.modules.conversations.protocols.IConversationService import IConversationService


class ConversationServiceFactory:
    def __init__(self, mongo_database: AsyncDatabase):
        self._mongo_database = mongo_database

    def get(self) -> IConversationService:
        return MongoConversationService(self._mongo_database)
