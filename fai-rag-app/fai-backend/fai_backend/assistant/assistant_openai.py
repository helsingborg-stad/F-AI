from typing import Callable, Any, Iterable

from langstream import Stream
from langstream.contrib import OpenAIChatStream, OpenAIChatDelta, OpenAIChatMessage

from fai_backend.assistant.models import LLMStreamDef, LLMStreamMessage
from fai_backend.assistant.protocol import IAssistantStreamProtocol


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
