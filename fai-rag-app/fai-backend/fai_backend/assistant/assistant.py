from typing import Any

from langstream import Stream

from fai_backend.assistant.models import AssistantTemplate
from fai_backend.assistant.protocol import ILLMProtocol, IAssistantStreamProtocol
from fai_backend.llm.service import create_rag_stream


class AssistantLLM(ILLMProtocol):
    def __init__(self, template: AssistantTemplate, base_stream: IAssistantStreamProtocol):
        self.template = template
        self.base_stream = base_stream
        self.vars = {}

    async def create(self) -> Stream[str, Any]:
        all_stream_producers = [self.base_stream.create_stream(stream_def, lambda: self.vars) for
                                stream_def in self.template.streams]

        chained_stream: Stream[str, Any] | None = None

        if self.template.files_collection_id:
            chained_stream = await self._create_rag_stream()

        for stream_producer in all_stream_producers:
            chained_stream = chained_stream.and_then(await stream_producer) \
                if chained_stream is not None \
                else await stream_producer

        def preprocess(initial_query: str):
            self.vars.update({"query": initial_query})
            return initial_query

        return (
            Stream[str, str]('preprocess', preprocess)
            .and_then(chained_stream)
        )

    async def _create_rag_stream(self) -> Stream[str, str]:
        async def run_rag_stream(initial_query: list[str]):
            stream = await create_rag_stream(initial_query[0], self.template.files_collection_id)
            async for r in stream(initial_query[0]):
                yield r

        def rag_postprocess(in_data: Any):
            results = in_data[0]['results']
            self.vars.update({'rag_results': results})
            return self.vars['query']

        return (
            Stream('RAGStream', run_rag_stream)
            .and_then(rag_postprocess)
        )
