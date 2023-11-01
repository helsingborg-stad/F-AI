from datetime import datetime
from pydantic import BaseModel, Field
from typing import List


class OutputTimestamp(BaseModel):
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)


class OutputFeedback(BaseModel):
    user: str
    rating: str
    comment: str = Field(default=None)
    timestamp: OutputTimestamp = OutputTimestamp()


class OutputMessageUserPermission(BaseModel):
    can_feedback: bool = False


class OutputMessage(BaseModel):
    user: str
    content: str
    feedback: List[OutputFeedback] = Field(default=[])
    timestamp: OutputTimestamp = OutputTimestamp()
    user_permissions: OutputMessageUserPermission = OutputMessageUserPermission()


class OutputConversationUserPermissions(BaseModel):
    can_read: bool = False
    can_message: bool = False
    can_feedback: bool = False


class OutputConversation(BaseModel):
    id: str
    created_by: str
    participants: List[str]
    messages: List[OutputMessage]
    timestamp: OutputTimestamp = OutputTimestamp()
    user_permissions: OutputConversationUserPermissions = (
        OutputConversationUserPermissions()
    )
