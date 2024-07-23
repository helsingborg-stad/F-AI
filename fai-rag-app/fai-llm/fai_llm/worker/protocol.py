from typing import Protocol

from fai_llm.assistant.models import AssistantStreamMessage, AssistantTemplate
from fai_llm.worker.model import OpaqueID, WorkStatus


class IWorkerService(Protocol):
    def enqueue(self, assistant: AssistantTemplate, history: list[AssistantStreamMessage], query: str) -> OpaqueID:
        ...

    def cancel(self, job_id: OpaqueID):
        ...

    def status(self, job_id: OpaqueID) -> WorkStatus:
        ...


class IWorkerFactory(Protocol):
    def create(self) -> IWorkerService:
        ...
