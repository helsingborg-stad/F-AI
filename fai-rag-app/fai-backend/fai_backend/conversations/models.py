import uuid
from typing import Optional, Annotated, List
from uuid import uuid4, UUID

from pydantic import BaseModel, Field, UUID4, BeforeValidator, ConfigDict
from bson import ObjectId as BsonObjectId, ObjectId
from pydantic.v1 import validator, root_validator

from fai_backend.schema import Timestamp


class Feedback(BaseModel):
    user: str
    created_by: str
    rating: str
    comment: str | None = None
    timestamp: Timestamp = Timestamp()


class Message(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    user: str
    content: str
    created_by: str
    type: str = 'message'
    feedback: list[Feedback] | None = Field(default_factory=list)
    timestamp: Timestamp = Timestamp()
    metadata: dict | None = Field(default_factory=dict)


class Conversation(BaseModel):
    id: ObjectId = Field(alias='_id')
    type: str = 'conversation'
    created_by: str
    participants: List[str]
    messages: List[Message] = Field(default_factory=list)
    conversation_id: UUID4 = Field(default_factory=uuid4)   # ID used to track the conversation and its copies
    conversation_root_id: UUID4 | None = None               # Any copy of the conversation will have the same root ID
    conversation_active_id: UUID4                           # The root conversation will track the active conversation
    timestamp: Timestamp = Timestamp()
    metadata: dict = Field(default_factory=dict)
    tags: List[str] | None = Field(default_factory=list)

    class Config:
        populate_by_name = True             # Populate model fields by name instead of alias if present
        arbitrary_types_allowed = True      # Allow arbitrary types (e.g. ObjectId)
        json_encoders = {ObjectId: str}     # `ObjectId` not serializable by default
        orm_mode = True

    @validator('id', pre=True, always=True)
    def ensure_object_id(cls, v):
        if isinstance(v, str):
            return ObjectId(v)
        return v
