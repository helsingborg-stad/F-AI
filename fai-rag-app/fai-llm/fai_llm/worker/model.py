from typing import Literal

from pydantic import BaseModel

from fai_llm.assistant.models import AssistantTemplate, AssistantStreamMessage

OpaqueID = str


class WorkStatus(BaseModel):
    status: Literal['pending', 'running', 'cancelled', 'done', 'failed']
    message: str


class WorkerMessages:
    class RunRequest(BaseModel):
        job_id: str
        assistant: AssistantTemplate
        history: list[AssistantStreamMessage]
        query: str

    class JobUpdate(BaseModel):
        job_id: OpaqueID
        message: str

    class JobDone(BaseModel):
        job_id: OpaqueID

    class JobError(BaseModel):
        job_id: OpaqueID
        error: str

    class ProcessCrash(BaseModel):
        error: str
