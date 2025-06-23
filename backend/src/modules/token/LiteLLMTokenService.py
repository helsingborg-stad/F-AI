from litellm import token_counter

from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.conversations.protocols.IConversationService import IConversationService
from src.modules.token.helpers.get_conversation_assistant_model import get_conversation_assistant_model
from src.modules.token.protocols.ITokenService import ITokenService


class LiteLLMTokenService(ITokenService):
    def __init__(self, assistant_service: IAssistantService, conversation_service: IConversationService):
        self._assistant_service = assistant_service
        self._conversation_service = conversation_service

    async def get_token_count(self, as_uid: str, assistant_id: str, message: str) -> int:
        assistant = await self._assistant_service.get_assistant(as_uid=as_uid, assistant_id=assistant_id,
                                                                redact_key=False)

        if not assistant:
            return -1

        tokens = token_counter(assistant.model, messages=[
            {'role': 'system', 'content': assistant.instructions},
            {'role': 'user', 'content': message},
        ])
        return tokens

    async def get_token_count_with_history(self, as_uid: str, conversation_id: str, message: str) -> int:
        fetched = await get_conversation_assistant_model(
            as_uid=as_uid,
            assistant_service=self._assistant_service,
            conversation_service=self._conversation_service,
            conversation_id=conversation_id
        )

        if not fetched:
            return -1

        conversation, assistant, model = fetched

        return token_counter(
            model,
            messages=[
                         {'role': m.role, 'content': m.content} for m in conversation.messages
                     ] + [{'role': 'user', 'content': message}]
        )
