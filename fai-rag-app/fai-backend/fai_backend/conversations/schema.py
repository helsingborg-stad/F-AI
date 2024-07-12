from uuid import uuid4

from bson import ObjectId
from pydantic import BaseModel, Field, UUID4

from fai_backend.conversations.models import Conversation, Feedback, Message


class FeedbackResponse(Feedback):
    pass


class ResponseMessage(Message):
    pass


class ConversationResponse(Conversation):
    messages: list[ResponseMessage]


class CreateFeedbackRequest(BaseModel):
    rating: str
    comment: str = None


class CreateMessageRequest(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    user: str = None
    created_by: str = None
    content: str = None
    type: str = 'message'
    metadata: dict = Field(default_factory=dict)


class CreateConversationRequest(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId)
    type: str = 'conversation'
    messages: list[CreateMessageRequest] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
    tags: list[str] | None = Field(default_factory=list)
    conversation_id: UUID4 = uuid4()
    conversation_root_id: UUID4 = None
    conversation_active_id: UUID4 = None

    def __init__(self, **data):
        super().__init__(**data)
        self.conversation_active_id = self.conversation_id

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
