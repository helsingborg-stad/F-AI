from typing import Protocol, Callable, Any

from langstream import Stream

from fai_backend.assistant.models import AssistantContext, AssistantStreamMessage, AssistantStreamInsert


class IAssistantContextStore(Protocol):
    def get_mutable(self) -> AssistantContext:
        ...


class IAssistantMessageInsert(Protocol):
    async def get_messages(self, context_store: IAssistantContextStore) -> list[AssistantStreamMessage]:
        pass


class IAssistantLLMProvider(Protocol):
    async def create_llm_stream(
            self,
            messages: list[AssistantStreamMessage | AssistantStreamInsert],
            context_store: IAssistantContextStore,
            get_insert: Callable[[str], IAssistantMessageInsert],
    ) -> Stream[list[str], str]:
        ...


class IAssistantPipelineStrategy(Protocol):
    async def create_pipeline(
            self,
            context_store: IAssistantContextStore
    ) -> Stream[list[str], str]:
        ...
