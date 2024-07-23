from fai_llm.assistant.assistant import Assistant
from fai_llm.assistant.models import AssistantContext, AssistantTemplate
from fai_llm.assistant.protocol import IAssistantContextStore


class AssistantFactory:
    def __init__(self):
        pass

    def create_assistant(self, template: AssistantTemplate) -> Assistant:
        assistant = Assistant(template, InMemoryAssistantContextStore())
        return assistant


class InMemoryAssistantContextStore(IAssistantContextStore):
    def __init__(self):
        self.context = AssistantContext()

    def get_mutable(self) -> AssistantContext:
        return self.context
