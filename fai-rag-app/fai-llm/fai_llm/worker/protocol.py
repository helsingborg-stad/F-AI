from typing import Protocol, Callable, Awaitable

from fai_llm.assistant.models import AssistantStreamMessage, AssistantTemplate
from fai_llm.worker.model import WorkStatus

WorkCallback = Callable[[WorkStatus], Awaitable[None]]


class IWorkerService(Protocol):
    def enqueue(
            self,
            job_id: str,
            assistant: AssistantTemplate,
            history: list[AssistantStreamMessage],
            query: str
    ) -> str:
        ...

    def cancel(self, job_id: str):
        ...

    async def listen_for(self, job_id: str, callback: WorkCallback):
        """
        Add a callback to be called when the job with the provided id is updated in any way.

        In case the job already has been started/completed the callback is called with the
        currently accumulated response.
        """
        ...

    def stop_listen_for(self, job_id: str):
        ...


class IWorkerFactory(Protocol):
    def create(self) -> IWorkerService:
        ...
