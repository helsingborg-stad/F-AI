from fai_backend.assistant.assistant import Assistant
from fai_backend.assistant.models import AssistantContext, AssistantTemplate
from fai_backend.assistant.protocol import IAssistantContextStore


class AssistantFactory:
    def __init__(self, assistant_templates: list[AssistantTemplate]):
        self.assistant_templates = assistant_templates

    def create_assistant(self, assistant_id) -> Assistant:
        template = next(a for a in self.assistant_templates if a.id == assistant_id)
        assistant = Assistant(template, InMemoryAssistantContextStore)
        return assistant


class InMemoryAssistantContextStore(IAssistantContextStore):
    def __init__(self):
        self.context = AssistantContext()

    def get_mutable(self) -> AssistantContext:
        return self.context
