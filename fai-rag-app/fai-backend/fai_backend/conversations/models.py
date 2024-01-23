from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

from schema import Timestamp


class Feedback(BaseModel):
    user: str
    rating: str
    comment: str | None = None
    timestamp: Timestamp = Timestamp()


class Message(BaseModel):
    user: str
    content: str
    feedback: list[Feedback] | None = Field(default_factory=list)
    timestamp: Timestamp = Timestamp()
    metadata: dict | None = Field(default_factory=dict)


class Conversation(BaseModel):
    id: Annotated[str, BeforeValidator(str)]
    created_by: str
    participants: list[str]
    messages: list[Message]
    timestamp: Timestamp = Timestamp()
    metadata: dict = Field(default_factory=dict)
    tags: list[str] | None = Field(default_factory=list)
