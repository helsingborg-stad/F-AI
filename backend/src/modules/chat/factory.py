from pymongo.asynchronous.database import AsyncDatabase

from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.chat.LLMChatService import LLMChatService
from src.modules.chat.MongoMessageStoreService import MongoMessageStoreService
from src.modules.chat.protocols.IChatService import IChatService
from src.modules.chat.protocols.IMessageStoreService import IMessageStoreService
from src.modules.conversations.protocols.IConversationService import IConversationService
from src.modules.llm.protocols.ILLMService import ILLMService


class ChatServiceFactory:
    def __init__(
            self,
            llm_service: ILLMService,
            assistant_service: IAssistantService,
            conversation_service: IConversationService
    ):
        self._llm_service = llm_service
        self._assistant_service = assistant_service
        self._conversation_service = conversation_service

    def get(self) -> IChatService:
        return LLMChatService(
            llm_service=self._llm_service,
            assistant_service=self._assistant_service,
            conversation_service=self._conversation_service
        )


class MessageStoreServiceFactory:
    def __init__(self, mongo_database: AsyncDatabase):
        self._mongo_database = mongo_database

    async def get(self) -> IMessageStoreService:
        service = MongoMessageStoreService(self._mongo_database)
        await service.init(expiry_seconds=30)
        return service
