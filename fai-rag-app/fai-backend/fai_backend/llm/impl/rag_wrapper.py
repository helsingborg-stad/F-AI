from langstream import Stream

from fai_backend.llm.protocol import ILLMStreamProtocol
from fai_backend.llm.models import LLMDataPacket
from fai_backend.llm.service import create_rag_stream


class RAGWrapper(ILLMStreamProtocol):
    """
    Wraps an underlying Stream with RAG capabilities.

    The underlying stream will be supplied with document extracts in plaintext
    from the given collection along with the original question.
    """

    def __init__(self, input_query: str, base_llm: ILLMStreamProtocol, rag_collection_name: str):
        self.input_query = input_query
        self.rag_collection_name = rag_collection_name
        self.base_llm = base_llm

    async def create(self) -> Stream[str, LLMDataPacket]:
        rag_stream = await create_rag_stream(self.input_query, self.rag_collection_name)
        base_stream = await self.base_llm.create()

        return (rag_stream
                .and_then(base_stream))
