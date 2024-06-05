from typing import Protocol, Iterable, Any, Callable

from langstream import Stream
from langstream.contrib import OpenAIChatStream, OpenAIChatDelta, OpenAIChatMessage

from fai_backend.assistant.models import AssistantTemplate, LLMStreamDef, LLMStreamMessage
from fai_backend.config import settings
from fai_backend.llm.protocol import ILLMStreamProtocol
from fai_backend.llm.service import create_rag_stream


class IAssistantStreamProtocol(Protocol):
    async def create_stream(self, stream_def: LLMStreamDef, get_vars: Callable[[], dict]) -> Stream[str, str]:
        """

        """


class OpenAIAssistantStream(IAssistantStreamProtocol):
    async def create_stream(self, stream_def: LLMStreamDef, get_vars: Callable[[], dict]) -> Stream[str, str]:
        return OpenAIChatStream[str, OpenAIChatDelta](
            stream_def.name,
            lambda in_data: self._to_openai_messages(in_data, stream_def.messages, get_vars),
            model=stream_def.settings.model,
            temperature=getattr(stream_def, 'settings.temperature', 0),
            functions=getattr(stream_def, 'functions', None),
            function_call=getattr(stream_def, 'function_call', None),
        ).map(lambda delta: delta.content)

    @staticmethod
    def _to_openai_messages(
            in_data: Any,
            messages: list[LLMStreamMessage],
            get_vars: Callable[[], dict]
    ) -> Iterable[OpenAIChatMessage]:
        def parse_in_data(data: Any):
            if isinstance(data, list):
                return "".join([parse_in_data(c) for c in data])
            return str(data)

        in_data_as_str = parse_in_data(in_data)

        input_vars = get_vars()
        input_vars['last_input'] = in_data_as_str

        return [OpenAIChatMessage(
            content=message.content.format(**input_vars),
            role=message.role
        ) for message in messages]


class AssistantLLM(ILLMStreamProtocol):
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


class AssistantFactory:
    def __init__(self, assistant_templates: list[AssistantTemplate]):
        self.assistant_templates = assistant_templates

    def create_assistant_stream(self, assistant_id: str, backend: str = settings.LLM_BACKEND) -> AssistantLLM:
        assistant = next(a for a in self.assistant_templates if a.id == assistant_id)
        return AssistantLLM(assistant, self._get_stream_constructor(backend))

    @staticmethod
    def _get_stream_constructor(backend: str) -> IAssistantStreamProtocol:
        return {
            'openai': lambda: OpenAIAssistantStream(),
        }[backend]()
