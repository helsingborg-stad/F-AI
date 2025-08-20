import json
import os
from typing import AsyncGenerator

from src.common.get_timestamp import get_timestamp
from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.assistants.reserved_ids import RAG_SCORING_ID
from src.modules.chat.models.ChatEvent import ChatEvent, ChatErrorEvent, ChatConversationIdEvent, ChatMessageEvent
from src.modules.chat.protocols.IChatService import IChatService
from src.modules.collections.protocols.ICollectionService import ICollectionService
from src.modules.conversations.models.Message import Message as ConversationMessage
from src.modules.conversations.protocols.IConversationService import IConversationService
from src.modules.ai.completions.factory import CompletionsServiceFactory
from src.modules.ai.completions.helpers.collect_streamed import collect_streamed
from src.modules.ai.completions.models.Feature import Feature
from src.modules.ai.completions.models.Message import Message as CompletionMessage
from src.modules.ai.completions.protocols.ICompletionsService import ICompletionsService


class LLMChatService(IChatService):
    def __init__(
            self,
            completions_factory: CompletionsServiceFactory,
            assistant_service: IAssistantService,
            conversation_service: IConversationService,
            collection_service: ICollectionService
    ):
        self._completions_factory = completions_factory
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
            yield ChatErrorEvent(message='invalid assistant')
            return

        conversation_id = await self._conversation_service.create_conversation(as_uid=as_uid, assistant_id=assistant_id)

        yield ChatConversationIdEvent(conversation_id=conversation_id)

        await self._conversation_service.add_message_to_conversation(
            as_uid=as_uid,
            conversation_id=conversation_id,
            message=ConversationMessage(
                timestamp=get_timestamp(),
                role='system',
                content=assistant.instructions
            )
        )

        async for m in self.continue_chat(as_uid=as_uid, conversation_id=conversation_id, message=message,
                                          enabled_features=enabled_features):
            yield m

    async def continue_chat(self, as_uid: str, conversation_id: str, message: str, enabled_features: list[Feature],
                            restart_from_id: str | None = None) -> \
            AsyncGenerator[ChatEvent, None]:
        conversation = await self._conversation_service.get_conversation(as_uid=as_uid, conversation_id=conversation_id)

        if not conversation:
            yield ChatErrorEvent(message='invalid conversation')
            return

        if restart_from_id is not None and next((m for m in conversation.messages if m.id == restart_from_id),
                                                None) is None:
            yield ChatErrorEvent(message='message to restart from not found')
            return

        assistant = await self._assistant_service.get_assistant(
            as_uid=as_uid,
            assistant_id=conversation.assistant_id,
            redact_key=False
        )

        if not assistant:
            yield ChatErrorEvent(message='invalid assistant')
            return

        await self._conversation_service.add_message_to_conversation(
            as_uid=as_uid,
            conversation_id=conversation_id,
            message=ConversationMessage(
                timestamp=get_timestamp(),
                role='user',
                content=message
            ),
            restart_from=restart_from_id,
        )

        rag_message: str | None = None

        if assistant.collection_id is not None:
            rag_scoring_assistant = await self._assistant_service.get_assistant(
                as_uid=os.environ['SETUP_ADMIN'],
                assistant_id=RAG_SCORING_ID)

            if rag_scoring_assistant is None:
                yield ChatErrorEvent(message='rag scoring assistant not found')
                return

            rag_service: ICompletionsService = self._completions_factory.get(model=rag_scoring_assistant.model,
                                                                             api_key=rag_scoring_assistant.llm_api_key)

            rag_results = await self._collection_service.query_collection(assistant.collection_id, message,
                                                                          max_results=assistant.max_collection_results)

            formatted_results = [f"(source:{r.source}, page: {r.page_number})\n{r.content}" for r in rag_results]

            async def _score_result(result: str) -> int:
                response = await collect_streamed(rag_service.run_completions(
                    messages=[
                        CompletionMessage(role='system', content=rag_scoring_assistant.instructions),
                        CompletionMessage(role='user', content=result)
                    ],
                    enabled_features=[],
                    extra_params=rag_scoring_assistant.extra_llm_params
                ))
                return int(json.loads(response.content)['score'])

            scored_results = [(fr, await _score_result(fr)) for fr in formatted_results]
            scored_results.sort(key=lambda x: x[1], reverse=True)

            SCORE_THRESHOLD = 70
            accurate_results = [r for r in scored_results if r[1] >= SCORE_THRESHOLD]

            rag_message = "Here are the results of the search:\n\n" + "\n\n".join([r[0] for r in accurate_results])

        try:
            completions_service = self._completions_factory.get(model=assistant.model, api_key=assistant.llm_api_key)
        except ValueError as e:
            yield ChatErrorEvent(message=str(e))
            return

        messages = [
            *[CompletionMessage(
                role=m.role,
                content=m.context_message_override if m.context_message_override else m.content,
                reasoning_content=m.reasoning_content,
                tool_call_id=m.tool_call_id,
                tool_calls=m.tool_calls,
            ) for m in conversation.messages],
            CompletionMessage(role='user', content=message),
            CompletionMessage(role='user', content=rag_message) if rag_message else None
        ]

        last_role = ''

        async for delta in completions_service.run_completions(
                messages=[m for m in messages if m],
                enabled_features=enabled_features,
                extra_params=assistant.extra_llm_params
        ):
            if delta.role != last_role:
                last_role = delta.role
                await self._conversation_service.add_message_to_conversation(
                    as_uid=as_uid,
                    conversation_id=conversation_id,
                    message=ConversationMessage(
                        timestamp=get_timestamp(),
                        role=delta.role,
                        content=delta.content,
                        reasoning_content=delta.reasoning_content,
                        tool_call_id=delta.tool_call_id,
                        tool_calls=delta.tool_calls,
                        context_message_override=delta.context_message_override
                    )
                )
            else:
                conversation = await self._conversation_service.get_conversation(as_uid=as_uid,
                                                                                 conversation_id=conversation_id)
                last_message = conversation.messages[-1]
                if delta.content is not None:
                    last_message.content = last_message.content + delta.content if last_message.content is not None else delta.content

                if delta.reasoning_content is not None:
                    last_message.reasoning_content = last_message.reasoning_content + delta.reasoning_content if last_message.reasoning_content is not None else delta.reasoning_content

                if delta.context_message_override is not None:
                    last_message.context_message_override = delta.context_message_override

                if delta.tool_calls is not None:
                    last_message.tool_calls = delta.tool_calls

                if delta.tool_call_id is not None:
                    last_message.tool_call_id = delta.tool_call_id

                await self._conversation_service.replace_conversation_last_message(
                    as_uid=as_uid,
                    conversation_id=conversation_id,
                    message=last_message
                )

            if delta.role == 'error':
                yield ChatErrorEvent(message=delta.content)
                return

            yield ChatMessageEvent(source=delta.role, message=delta.content, reasoning=delta.reasoning_content)
