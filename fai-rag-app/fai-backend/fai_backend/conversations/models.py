from uuid import uuid4

from pydantic import BaseModel, Field, UUID4

from fai_backend.schema import Timestamp


class Feedback(BaseModel):
    user: str
    created_by: str
    rating: str
    comment: str | None = None
    timestamp: Timestamp = Timestamp()


class Message(BaseModel):
    user: str
    content: str
    created_by: str
    type: str = 'message'
    feedback: list[Feedback] | None = Field(default_factory=list)
    timestamp: Timestamp = Timestamp()
    metadata: dict | None = Field(default_factory=dict)


class Thread(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    thread_name: str
    copy_of_thread_with_id: str | None = None
    active_flag: bool
    timestamp: Timestamp = Timestamp()
    messages: list[Message]
    feedback: Feedback | None = None
    metadata: dict | None = Field(default_factory=dict)


class Conversation(BaseModel):
    id: str
    type: str = 'conversation'
    created_by: str
    participants: list[str]
    threads: list[Thread]
    messages: list[Message]
    timestamp: Timestamp = Timestamp()
    metadata: dict = Field(default_factory=dict)
    tags: list[str] | None = Field(default_factory=list)
