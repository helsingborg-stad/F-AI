from pydantic import BaseModel, Field

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
    user: str = None
    created_by: str = None
    content: str = None
    type: str = 'message'
    metadata: dict = Field(default_factory=dict)


class CreateConversationRequest(BaseModel):
    project_id: str
    messages: list[CreateMessageRequest]
    metadata: dict = Field(default_factory=dict)
