from typing import Protocol

from langstream import Stream

from fai_backend.llm.models import LLMDataPacket


class ILLMStreamProtocol(Protocol):
    async def create(self) -> Stream[str, LLMDataPacket]:
        """
        Create a Stream that takes a str (generally a question) and returns
        a stream of tokens (strings) of the response given by the LLM.
        """
        ...
