import json
import os
from typing import AsyncGenerator

from src.common.get_timestamp import get_timestamp
from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.assistants.reserved_ids import RAG_SCORING_ID
from src.modules.chat.models.ChatEvent import ChatEvent
from src.modules.chat.protocols.IChatService import IChatService
from src.modules.collections.protocols.ICollectionService import ICollectionService
from src.modules.conversations.protocols.IConversationService import IConversationService
from src.modules.llm.factory import LLMServiceFactory
from src.modules.llm.helpers.collect_streamed import collect_streamed
from src.modules.llm.models.Feature import Feature
from src.modules.llm.models.Message import Message
from src.modules.llm.protocols.ILLMService import ILLMService


class LLMChatService(IChatService):
    def __init__(
            self,
            llm_factory: LLMServiceFactory,
            assistant_service: IAssistantService,
            conversation_service: IConversationService,
            collection_service: ICollectionService
    ):
        self._llm_factory = llm_factory
        self._assistant_service = assistant_service
        self._conversation_service = conversation_service
        self._collection_service = collection_service

    async def start_new_chat(self, as_uid: str, assistant_id: str, message: str, enabled_features: list[Feature]) -> \
            AsyncGenerator[ChatEvent, None]:
        assistant = await self._assistant_service.get_assistant(
            as_uid=as_uid,
            assistant_id=assistant_id,
            redact_key=False
        )

        if not assistant:
            yield ChatEvent(event='error', message='invalid assistant')
            return

        conversation_id = await self._conversation_service.create_conversation(as_uid=as_uid, assistant_id=assistant_id)

        yield ChatEvent(event='conversation_id', conversation_id=conversation_id)

        await self._conversation_service.add_message_to_conversation(
            as_uid=as_uid,
            conversation_id=conversation_id,
            timestamp=get_timestamp(),
            role='system',
            message=assistant.instructions
        )

        async for m in self.continue_chat(as_uid=as_uid, conversation_id=conversation_id, message=message,
                                          enabled_features=enabled_features):
            yield m

    async def continue_chat(self, as_uid: str, conversation_id: str, message: str, enabled_features: list[Feature]) -> \
            AsyncGenerator[ChatEvent, None]:
        conversation = await self._conversation_service.get_conversation(as_uid=as_uid, conversation_id=conversation_id)

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
            as_uid=as_uid,
            conversation_id=conversation_id,
            timestamp=get_timestamp(),
            role='user',
            message=message
        )

        rag_message: str | None = None

        if assistant.collection_id is not None:
            rag_scoring_assistant = await self._assistant_service.get_assistant(
                as_uid=os.environ['SETUP_ADMIN'],
                assistant_id=RAG_SCORING_ID)

            if rag_scoring_assistant is None:
                yield ChatEvent(event='error', message='rag scoring assistant not found')
                return

            rag_llm_service: ILLMService = self._llm_factory.get()

            rag_results = await self._collection_service.query_collection(assistant.collection_id, message,
                                                                          max_results=assistant.max_collection_results)

            formatted_results = [f"(source:{r.source}, page: {r.page_number})\n{r.content}" for r in rag_results]

            async def _score_result(result: str) -> int:
                response = await collect_streamed(rag_llm_service.run(
                    model=rag_scoring_assistant.model,
                    messages=[
                        Message(role='system', content=rag_scoring_assistant.instructions),
                        Message(role='user', content=result)
                    ],
                    api_key=rag_scoring_assistant.llm_api_key,
                    enabled_features=[],
                    extra_params=rag_scoring_assistant.extra_llm_params
                ))
                return int(json.loads(response.content)['score'])

            scored_results = [(fr, await _score_result(fr)) for fr in formatted_results]
            scored_results.sort(key=lambda x: x[1], reverse=True)

            SCORE_THRESHOLD = 70
            accurate_results = [r for r in scored_results if r[1] >= SCORE_THRESHOLD]

            rag_message = "Here are the results of the search:\n\n" + "\n\n".join([r[0] for r in accurate_results])

        await self._conversation_service.add_message_to_conversation(
            as_uid=as_uid,
            conversation_id=conversation_id,
            timestamp=get_timestamp(),
            role='',
            message=''
        )

        try:
            llm_service = self._llm_factory.get()
        except ValueError as e:
            yield ChatEvent(event='error', source='error',
                            message=str(e))
            return

        messages = [
            *[Message(role=m.role, content=m.content) for m in conversation.messages],
            Message(role='user', content=message),
            Message(role='user', content=rag_message) if rag_message else None
        ]

        async for delta in llm_service.run(
                model=assistant.model,
                api_key=assistant.llm_api_key,
                messages=[m for m in messages if m],
                enabled_features=enabled_features,
                extra_params=assistant.extra_llm_params
        ):
            if delta.role != 'error' and delta.content is not None:
                await self._conversation_service.add_to_conversation_last_message(
                    as_uid=as_uid,
                    conversation_id=conversation_id,
                    timestamp=get_timestamp(),
                    role=delta.role,
                    additional_message=delta.content
                )

            yield ChatEvent(event='error' if delta.role == 'error' else 'message', source=delta.role,
                            message=delta.content, reasoning=delta.reasoning_content)
