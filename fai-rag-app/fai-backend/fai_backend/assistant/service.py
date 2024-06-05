from fai_backend.assistant.assistant import AssistantLLM
from fai_backend.assistant.assistant_openai import OpenAIAssistantStream
from fai_backend.assistant.models import AssistantTemplate
from fai_backend.config import settings
from fai_backend.assistant.protocol import IAssistantStreamProtocol


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
