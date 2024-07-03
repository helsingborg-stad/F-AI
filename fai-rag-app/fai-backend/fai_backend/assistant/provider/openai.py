from typing import Iterable

from langstream import Stream
from langstream.contrib import OpenAIChatStream, OpenAIChatDelta, OpenAIChatMessage
from pydantic import BaseModel

from fai_backend.assistant.models import AssistantStreamMessage
from fai_backend.assistant.protocol import IAssistantLLMProvider, IAssistantContextStore


class OpenAIAssistantLLMProvider(IAssistantLLMProvider):
    class Settings(BaseModel):
        model: str
        temperature: float = 0

    def __init__(self, settings: Settings):
        self.settings = settings

    async def create_llm_stream(
            self,
            messages: list[AssistantStreamMessage],
            context_store: IAssistantContextStore
    ) -> Stream[str, str]:
        return OpenAIChatStream[str, OpenAIChatDelta](
            "openai",
            lambda in_data: self._to_openai_messages(messages, context_store),
            **self.settings.dict(),
        ).map(lambda delta: delta.content)

    @staticmethod
    def _to_openai_messages(
            messages: list[AssistantStreamMessage],
            context_store: IAssistantContextStore
    ) -> Iterable[OpenAIChatMessage]:
        context = context_store.get_mutable()
        return [OpenAIChatMessage(
            content=message.content.format(**context.dict()),
            role=message.role
        ) for message in messages]
