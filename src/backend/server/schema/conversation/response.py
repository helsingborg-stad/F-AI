from ..common.output import OutputTimestamp


from pydantic import BaseModel


from typing import List, Optional


class OutputFeedback(BaseModel):
    user: str
    rating: str
    comment: Optional[str] = None
    timestamp: OutputTimestamp = OutputTimestamp()

class OutputMessageUserPermission(BaseModel):
    can_feedback: bool = False

class OutputMessage(BaseModel):
    user: str
    content: str
    feedback: Optional[List[OutputFeedback]] = []
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
    user_permissions: OutputConversationUserPermissions = OutputConversationUserPermissions()
    
