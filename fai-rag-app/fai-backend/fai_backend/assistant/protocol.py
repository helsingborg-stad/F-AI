from typing import Protocol, Callable

from langstream import Stream

from fai_backend.assistant.models import LLMStreamDef


class ILLMProtocol(Protocol):
    async def create(self) -> Stream[str, str]:
        """
        Create a Stream that takes a str (generally a question) and returns
        a stream of tokens (strings) of the response given by the LLM.
        """
        ...


class IAssistantStreamProtocol(Protocol):
    async def create_stream(self, stream_def: LLMStreamDef, get_vars: Callable[[], dict]) -> Stream[str, str]:
        ...
