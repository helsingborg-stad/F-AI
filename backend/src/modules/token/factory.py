from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.conversations.protocols.IConversationService import IConversationService
from src.modules.token.LiteLLMTokenService import LiteLLMTokenService
from src.modules.token.protocols.ITokenService import ITokenService


class TokenServiceFactory:
    def __init__(self, assistant_service: IAssistantService, conversation_service: IConversationService):
        self._assistant_service = assistant_service
        self._conversation_service = conversation_service

    def get(self) -> ITokenService:
        return LiteLLMTokenService(self._assistant_service, self._conversation_service)
