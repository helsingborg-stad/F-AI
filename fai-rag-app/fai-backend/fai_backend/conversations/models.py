from typing import Optional

from pydantic import BaseModel

from fai_backend.schema import Timestamp


class InputFeedbackModel(BaseModel):
    user: str
    rating: str
    comment: Optional[str] = None


class InputMessageModel(BaseModel):
    user: str
    content: str
    feedback: Optional[list[InputFeedbackModel]] = []


class InputConversationModel(BaseModel):
    created_by: str
    messages: list[InputMessageModel]
    participants: list[str]


class FeedbackModel(BaseModel):
    user: str
    rating: str
    comment: Optional[str] = None
    timestamp: Timestamp = Timestamp()


class MessageModel(BaseModel):
    user: str
    content: str
    feedback: Optional[list[FeedbackModel]] = []
    timestamp: Timestamp = Timestamp()


class ConversationModel(BaseModel):
    id: str
    created_by: str
    participants: list[str]
    messages: list[MessageModel]
    timestamp: Timestamp = Timestamp()
