from typing import Protocol

from langstream import Stream

from fai_backend.assistant.models import AssistantContext, AssistantStreamMessage


class IAssistantContextStore(Protocol):
    def get_mutable(self) -> AssistantContext:
        ...


class IAssistantLLMProvider(Protocol):
    async def create_llm_stream(
            self,
            messages: list[AssistantStreamMessage],
            context_store: IAssistantContextStore
    ) -> Stream[str, str]:
        ...


class IAssistantPipelineStrategy(Protocol):
    async def create_pipeline(
            self,
            context_store: IAssistantContextStore
    ) -> Stream[str, str]:
        ...
