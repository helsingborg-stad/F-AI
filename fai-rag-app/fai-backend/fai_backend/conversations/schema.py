from pydantic import BaseModel, Field

from conversations.models import Conversation
from fai_backend.schema import Timestamp


class FeedbackResponse(BaseModel):
    user: str
    rating: str
    comment: str = Field(default=None)
    timestamp: Timestamp = Timestamp()
    metadata: dict = Field(default_factory=dict)


class ResponseMessageUserPermission(BaseModel):
    can_feedback: bool = False


class ResponseMessage(BaseModel):
    user: str
    content: str
    feedback: list[FeedbackResponse] = Field(default=[])
    timestamp: Timestamp = Timestamp()
    user_permissions: ResponseMessageUserPermission = ResponseMessageUserPermission()
    metadata: dict = Field(default_factory=dict)


class ConversationUserPermissionsResponse(BaseModel):
    can_read: bool = False
    can_message: bool = False
    can_feedback: bool = False


class ConversationResponse(Conversation):
    user_permissions: ConversationUserPermissionsResponse = (
        ConversationUserPermissionsResponse()
    )
    metadata: dict = Field(default_factory=dict)


class CreateFeedbackRequest(BaseModel):
    rating: str
    comment: str = None


class CreateMessageRequest(BaseModel):
    user: str = None
    content: str = None
    metadata: dict = Field(default_factory=dict)


class CreateConversationRequest(BaseModel):
    project_id: str
    messages: list[CreateMessageRequest]
    metadata: dict = Field(default_factory=dict)
