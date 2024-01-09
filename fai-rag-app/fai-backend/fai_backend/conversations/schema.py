from pydantic import BaseModel, Field

from fai_backend.schema import Timestamp


class ResponseFeedback(BaseModel):
    user: str
    rating: str
    comment: str = Field(default=None)
    timestamp: Timestamp = Timestamp()


class ResponseMessageUserPermission(BaseModel):
    can_feedback: bool = False


class ResponseMessage(BaseModel):
    user: str
    content: str
    feedback: list[ResponseFeedback] = Field(default=[])
    timestamp: Timestamp = Timestamp()
    user_permissions: ResponseMessageUserPermission = ResponseMessageUserPermission()


class ResponseConversationUserPermissions(BaseModel):
    can_read: bool = False
    can_message: bool = False
    can_feedback: bool = False


class ResponseConversation(BaseModel):
    id: str
    created_by: str
    participants: list[str]
    messages: list[ResponseMessage]
    timestamp: Timestamp = Timestamp()
    user_permissions: ResponseConversationUserPermissions = (
        ResponseConversationUserPermissions()
    )


class RequestFeedback(BaseModel):
    comment: str = Field(default=None)
    rating: str


class RequestMessage(BaseModel):
    user: str = Field(default=None)
    content: str = Field(default=None)


class RequestConversation(BaseModel):
    messages: list[RequestMessage]
    project_id: str
