from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class TimestampModel(BaseModel):
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)


class FeedbackModel(BaseModel):
    user: str
    rating: str
    comment: Optional[str] = None
    timestamp: TimestampModel = TimestampModel()


class MessageModel(BaseModel):
    user: str
    content: str
    feedback: Optional[List[FeedbackModel]] = []
    timestamp: TimestampModel = TimestampModel()


class ConversationModel(BaseModel):
    id: str
    created_by: str
    participants: List[str]
    messages: List[MessageModel]
    timestamp: TimestampModel = TimestampModel()


class InsertFeedbackModel(BaseModel):
    user: str
    rating: str
    comment: Optional[str] = None


class InsertMessageModel(BaseModel):
    user: str
    content: str
    feedback: Optional[List[FeedbackModel]] = []


class InsertConversationModel(BaseModel):
    created_by: str
    messages: List[InsertMessageModel]
    participants: List[str]
