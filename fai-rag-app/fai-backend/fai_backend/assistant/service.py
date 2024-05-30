from typing import Protocol

from langstream import Stream
from langstream.contrib import OpenAIChatStream, OpenAIChatDelta

from fai_backend.assistant.models import AssistantTemplate, LLMStream
from fai_backend.config import settings
from fai_backend.llm.models import LLMDataPacket
from fai_backend.llm.protocol import ILLMStreamProtocol


class IAssistantStreamProtocol(Protocol):
    async def create(self, model: LLMStream) -> Stream[str, LLMDataPacket]:
        """

        """


class OpenAIAssistantStream(IAssistantStreamProtocol):
    async def create(self, model: LLMStream) -> Stream[str, LLMDataPacket]:
        return OpenAIChatStream[str, OpenAIChatDelta](
            model.name,
            model.messages,
            model=model.settings.model,
            temperature=model.settings.temperature or 0,
            functions=model.functions,
            function_call=model.function_call
        ).map(lambda delta: LLMDataPacket(content=delta.content, user_friendly=True))


class AssistantLLM(ILLMStreamProtocol):
    def __init__(self, template: AssistantTemplate, base_stream: IAssistantStreamProtocol):
        self.template = template
        self.base_stream = base_stream

    async def create(self) -> Stream[str, LLMDataPacket]:
        all_streams = [self.base_stream.create(model) for model in self.template.streams]

        final_stream: Stream[str, LLMDataPacket] | None = None

        for stream in all_streams:
            final_stream = final_stream.and_then(await stream) if final_stream else await stream

        return final_stream


class AssistantFactory:
    def __init__(self, assistant_templates: [AssistantTemplate]):
        self.assistant_templates = assistant_templates

    def create_assistant_stream(self, assistant_name: str, backend: str = settings.LLM_BACKEND) -> ILLMStreamProtocol:
        assistant = [a for a in self.assistant_templates if a.name == assistant_name][0]
        return AssistantLLM(assistant, self._get_stream_constructor(backend))

    @staticmethod
    def _get_stream_constructor(backend: str) -> IAssistantStreamProtocol:
        return {
            'openai': lambda: OpenAIAssistantStream(),
        }[backend]()
