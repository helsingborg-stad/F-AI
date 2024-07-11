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


class CreateThreadRequest(BaseModel):
    thread_name: str
    copy_of_thread_with_id: str = None
    active_flag: bool
    messages: list[CreateMessageRequest]
    feedback: CreateFeedbackRequest = None
    metadata: dict | None = Field(default_factory=dict)


class CreateConversationRequest(BaseModel):
    project_id: str
    threads: list[CreateThreadRequest] | None = Field(default_factory=list)
    messages: list[CreateMessageRequest]
    metadata: dict = Field(default_factory=dict)
    tags: list[str] | None = Field(default_factory=list)
