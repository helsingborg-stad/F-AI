from typing import AsyncGenerator

from src.common.get_timestamp import get_timestamp
from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.chat.models.ChatEvent import ChatEvent
from src.modules.chat.protocols.IChatService import IChatService
from src.modules.conversations.protocols.IConversationService import IConversationService
from src.modules.llm.models.Message import Message
from src.modules.llm.protocols.ILLMService import ILLMService


class LLMChatService(IChatService):
    def __init__(
            self,
            llm_service: ILLMService,
            assistant_service: IAssistantService,
            conversation_service: IConversationService
    ):
        self._llm_service = llm_service
        self._assistant_service = assistant_service
        self._conversation_service = conversation_service

    async def start_new_chat(self, as_uid: str, assistant_id: str, message: str) -> AsyncGenerator[ChatEvent, None]:
        assistant = await self._assistant_service.get_assistant(
            as_uid=as_uid,
            assistant_id=assistant_id,
            redact_key=False
        )

        if not assistant:
            yield ChatEvent(event='error', message='invalid assistant')
            return

        conversation_id = await self._conversation_service.create_conversation(assistant_id=assistant_id)

        yield ChatEvent(event='conversation_id', conversation_id=conversation_id)

        await self._conversation_service.add_message_to_conversation(
            conversation_id=conversation_id,
            timestamp=get_timestamp(),
            role='system',
            message=assistant.instructions
        )

        async for m in self.continue_chat(as_uid=as_uid, conversation_id=conversation_id, message=message):
            yield m

    async def continue_chat(self, as_uid: str, conversation_id: str, message: str) -> AsyncGenerator[ChatEvent, None]:
        conversation = await self._conversation_service.get_conversation(conversation_id)

        if not conversation:
            yield ChatEvent(event='error', message='invalid conversation')
            return

        assistant = await self._assistant_service.get_assistant(
            as_uid=as_uid,
            assistant_id=conversation.assistant_id,
            redact_key=False
        )

        if not assistant:
            yield ChatEvent(event='error', message='invalid assistant')
            return

        await self._conversation_service.add_message_to_conversation(
            conversation_id=conversation_id,
            timestamp=get_timestamp(),
            role='user',
            message=message
        )

        await self._conversation_service.add_message_to_conversation(
            conversation_id=conversation_id,
            timestamp=get_timestamp(),
            role='',
            message=''
        )

        async for delta in self._llm_service.stream_llm(
                model=assistant.model,
                messages=[
                    *[Message(role=m.role, content=m.content) for m in conversation.messages],
                    Message(role='user', content=message)
                ],
                max_tokens=assistant.max_tokens,
                temperature=assistant.temperature,
                api_key=assistant.llm_api_key,
        ):
            if delta.role != 'error':
                await self._conversation_service.add_to_conversation_last_message(
                    conversation_id=conversation_id,
                    timestamp=get_timestamp(),
                    role=delta.role,
                    additional_message=delta.content
                )

            yield ChatEvent(event='error' if delta.role == 'error' else 'message', source=delta.role,
                            message=delta.content)
