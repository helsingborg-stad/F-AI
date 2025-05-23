from pymongo.asynchronous.database import AsyncDatabase

from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.chat.LLMChatService import LLMChatService
from src.modules.chat.MongoMessageStoreService import MongoMessageStoreService
from src.modules.chat.protocols.IChatService import IChatService
from src.modules.chat.protocols.IMessageStoreService import IMessageStoreService
from src.modules.collections.protocols.ICollectionService import ICollectionService
from src.modules.conversations.protocols.IConversationService import IConversationService
from src.modules.llm.factory import LLMServiceFactory


class ChatServiceFactory:
    def __init__(
            self,
            llm_factory: LLMServiceFactory,
            assistant_service: IAssistantService,
            conversation_service: IConversationService,
            collection_service: ICollectionService,
    ):
        self._llm_factory = llm_factory
        self._assistant_service = assistant_service
        self._conversation_service = conversation_service
        self._collection_service = collection_service

    def get(self) -> IChatService:
        return LLMChatService(
            llm_factory=self._llm_factory,
            assistant_service=self._assistant_service,
            conversation_service=self._conversation_service,
            collection_service=self._collection_service
        )


class MessageStoreServiceFactory:
    def __init__(self, mongo_database: AsyncDatabase):
        self._mongo_database = mongo_database

    async def get(self) -> IMessageStoreService:
        service = MongoMessageStoreService(self._mongo_database)
        await service.init(expiry_seconds=30)
        return service
