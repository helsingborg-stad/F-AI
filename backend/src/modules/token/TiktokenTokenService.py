import tiktoken

from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.conversations.protocols.IConversationService import IConversationService
from src.modules.llm.helpers.parse_model_key import parse_model_key
from src.modules.token.helpers.get_conversation_assistant_model import get_conversation_assistant_model
from src.modules.token.protocols.ITokenService import ITokenService


class TiktokenTokenService(ITokenService):
    def __init__(self, assistant_service: IAssistantService, conversation_service: IConversationService):
        self._assistant_service = assistant_service
        self._conversation_service = conversation_service

    @staticmethod
    async def _get_tokens(model_name: str, messages: list[str]):
        try:
            encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            encoding = tiktoken.get_encoding("o200k_base")  # Fallback - used by many 4o/oX variants
        lengths = [len(encoding.encode(msg)) for msg in messages]
        return sum(lengths)

    async def get_token_count(self, as_uid: str, assistant_id: str, message: str) -> int:
        assistant = await self._assistant_service.get_assistant(as_uid=as_uid, assistant_id=assistant_id)

        if not assistant:
            return -1

        [_, model_name] = parse_model_key(assistant.model)
        messages = [assistant.instructions, message]

        return await self._get_tokens(model_name, messages)

    async def get_token_count_with_history(self, as_uid: str, conversation_id: str, message: str) -> int:
        fetched = await get_conversation_assistant_model(
            as_uid=as_uid,
            assistant_service=self._assistant_service,
            conversation_service=self._conversation_service,
            conversation_id=conversation_id
        )

        if not fetched:
            return -1

        conversation, assistant, model_name = fetched

        conversation_messages = [m.content for m in conversation.messages]
        messages = [*conversation_messages, message]

        return await self._get_tokens(model_name, messages)
