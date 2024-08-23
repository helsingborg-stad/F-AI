from typing import Callable, Any

from langstream import Stream
from langstream.contrib import OpenAIChatStream, OpenAIChatDelta, OpenAIChatMessage
from pydantic import BaseModel

from fai_backend.assistant.helper import messages_expander_stream
from fai_backend.assistant.models import AssistantStreamMessage, AssistantStreamInsert
from fai_backend.assistant.protocol import IAssistantLLMProvider, IAssistantContextStore, IAssistantMessageInsert


class OpenAIAssistantLLMProvider(IAssistantLLMProvider):
    class Settings(BaseModel):
        model: str
        temperature: float = 0

    def __init__(self, settings: Settings, stream_class=OpenAIChatStream[str, OpenAIChatDelta]):
        self.settings = settings
        self._stream_class = stream_class

    async def create_llm_stream(
            self,
            messages: list[AssistantStreamMessage | AssistantStreamInsert],
            context_store: IAssistantContextStore,
            get_insert: Callable[[str], IAssistantMessageInsert],
    ) -> Stream[Any, Any]:
        def convert_messages(in_list: list[AssistantStreamMessage]):
            converted = [self._to_openai_message(m, context_store) for m in in_list]
            return converted

        main_stream = self._stream_class(
            "openai",
            lambda in_data: convert_messages(in_data[0]),
            **self.settings.dict(),
        ).map(lambda delta: delta.content)

        return messages_expander_stream(messages, context_store, get_insert).and_then(main_stream)

    @staticmethod
    def _to_openai_message(message: AssistantStreamMessage, context_store: IAssistantContextStore):
        context = context_store.get_mutable()
        return OpenAIChatMessage(
            content=message.content.format(**context.dict()),
            role=message.role
        )

    @staticmethod
    async def _parse_messages(
            messages: list[AssistantStreamMessage | AssistantStreamInsert],
            context_store: IAssistantContextStore,
            get_insert: Callable[[str], IAssistantMessageInsert]
    ):
        context = context_store.get_mutable()

        async def parse_one_message(
                message: AssistantStreamMessage | AssistantStreamInsert
        ) -> list[OpenAIChatMessage]:
            if isinstance(message, AssistantStreamMessage):
                return [OpenAIChatMessage(
                    content=message.content.format(**context.dict()),
                    role=message.role
                )]
            insert_messages = await get_insert(message.insert).get_messages(context_store)
            return [OpenAIChatMessage(role=m.role, content=m.content) for m in insert_messages]

        parsed_message_lists = [await parse_one_message(m) for m in messages]
        return [item for sublist in parsed_message_lists for item in sublist]
