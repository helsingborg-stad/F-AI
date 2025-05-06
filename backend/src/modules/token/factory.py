from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.conversations.protocols.IConversationService import IConversationService
from src.modules.llm.helpers.parse_model_key import parse_model_key
from src.modules.token.protocols.ITokenService import ITokenService


class TokenServiceFactory:
    def __init__(self, assistant_service: IAssistantService, conversation_service: IConversationService):
        self._assistant_service = assistant_service
        self._conversation_service = conversation_service

    def get(self, model_key: str) -> ITokenService:
        (provider, _) = parse_model_key(model_key)

        match provider:
            case 'openai':
                from src.modules.token.TiktokenTokenService import TiktokenTokenService
                return TiktokenTokenService(self._assistant_service, self._conversation_service)
            case 'anthropic':
                from src.modules.token.AnthropicTokenService import AnthropicTokenService
                return AnthropicTokenService(self._assistant_service, self._conversation_service)
            case _:
                raise ValueError(f'No valid token service for model with key {model_key}')
