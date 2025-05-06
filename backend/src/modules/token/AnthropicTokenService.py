import anthropic
from anthropic.types import MessageParam

from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.conversations.protocols.IConversationService import IConversationService
from src.modules.llm.helpers.parse_model_key import parse_model_key
from src.modules.token.protocols.ITokenService import ITokenService


class AnthropicTokenService(ITokenService):
    def __init__(self, assistant_service: IAssistantService, conversation_service: IConversationService):
        self._assistant_service = assistant_service
        self._conversation_service = conversation_service

    async def get_token_count(self, as_uid: str, assistant_id: str, message: str) -> int:
        assistant = await self._assistant_service.get_assistant(as_uid=as_uid, assistant_id=assistant_id,
                                                                redact_key=False)

        if not assistant:
            return -1

        [_, model_name] = parse_model_key(assistant.model)

        client = anthropic.AsyncAnthropic(api_key=assistant.llm_api_key)

        response = await client.messages.count_tokens(
            model=model_name,
            system=assistant.instructions,
            messages=[MessageParam(role='user', content=message)]
        )

        return response.input_tokens

    async def get_token_count_with_history(self, as_uid: str, conversation_id: str, message: str) -> int:
        conversation = await self._conversation_service.get_conversation(as_uid=as_uid, conversation_id=conversation_id)

        if not conversation:
            return -1

        assistant = await self._assistant_service.get_assistant(as_uid=as_uid, assistant_id=conversation.assistant_id,
                                                                redact_key=False)

        if not assistant:
            return -1

        [_, model_name] = parse_model_key(assistant.model)

        client = anthropic.AsyncAnthropic(api_key=assistant.llm_api_key)

        response = await client.messages.count_tokens(
            model=model_name,
            system=assistant.instructions,
            messages=[
                MessageParam(
                    role=m.role if m.role in ['user', 'assistant'] else 'user',
                    content=m.content
                )
                for m in conversation.messages
                if m.role != 'system'
            ] + [MessageParam(role='user', content=message)]
        )

        return response.input_tokens
