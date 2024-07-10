from typing import Callable

from langstream import Stream
from langstream.contrib import OpenAIChatStream, OpenAIChatDelta, OpenAIChatMessage
from pydantic import BaseModel

from fai_backend.assistant.models import AssistantStreamMessage, AssistantStreamInsert
from fai_backend.assistant.protocol import IAssistantLLMProvider, IAssistantContextStore, IAssistantMessageInsert


class OpenAIAssistantLLMProvider(IAssistantLLMProvider):
    class Settings(BaseModel):
        model: str
        temperature: float = 0

    def __init__(self, settings: Settings):
        self.settings = settings

    async def create_llm_stream(
            self,
            messages: list[AssistantStreamMessage | AssistantStreamInsert],
            context_store: IAssistantContextStore,
            get_insert: Callable[[str], IAssistantMessageInsert],
    ) -> Stream[list[str], str]:
        return OpenAIChatStream[str, OpenAIChatDelta](
            "openai",
            lambda in_data: self._parse_messages(messages, context_store, get_insert),
            **self.settings.dict(),
        ).map(lambda delta: delta.content)

    @staticmethod
    def _parse_messages(
            messages: list[AssistantStreamMessage | AssistantStreamInsert],
            context_store: IAssistantContextStore,
            get_insert: Callable[[str], IAssistantMessageInsert]
    ):
        context = context_store.get_mutable()

        def parse_one_message(
                message: AssistantStreamMessage | AssistantStreamInsert
        ) -> list[OpenAIChatMessage]:
            if isinstance(message, AssistantStreamMessage):
                return [OpenAIChatMessage(
                    content=message.content.format(**context.dict()),
                    role=message.role
                )]
            insert_messages = get_insert(message.insert).get_messages(context_store)
            return [OpenAIChatMessage(role=m.role, content=m.content) for m in insert_messages]

        parsed_message_lists = [parse_one_message(m) for m in messages]
        return [item for sublist in parsed_message_lists for item in sublist]
