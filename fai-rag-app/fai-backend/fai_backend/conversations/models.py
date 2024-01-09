from typing import List, Optional

from pydantic import BaseModel

from fai_backend.schema import Timestamp


class InputFeedbackModel(BaseModel):
    user: str
    rating: str
    comment: Optional[str] = None


class InputMessageModel(BaseModel):
    user: str
    content: str
    feedback: Optional[List[InputFeedbackModel]] = []


class InputConversationModel(BaseModel):
    created_by: str
    messages: List[InputMessageModel]
    participants: List[str]


class FeedbackModel(BaseModel):
    user: str
    rating: str
    comment: Optional[str] = None
    timestamp: Timestamp = Timestamp()


class MessageModel(BaseModel):
    user: str
    content: str
    feedback: Optional[List[FeedbackModel]] = []
    timestamp: Timestamp = Timestamp()


class ConversationModel(BaseModel):
    id: str
    created_by: str
    participants: List[str]
    messages: List[MessageModel]
    timestamp: Timestamp = Timestamp()
