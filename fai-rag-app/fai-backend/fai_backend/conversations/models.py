
from pydantic import BaseModel

from fai_backend.schema import Timestamp


class InputFeedbackModel(BaseModel):
    user: str
    rating: str
    comment: str | None = None


class InputMessageModel(BaseModel):
    user: str
    content: str
    feedback: list[InputFeedbackModel] | None = []


class InputConversationModel(BaseModel):
    created_by: str
    messages: list[InputMessageModel]
    participants: list[str]


class FeedbackModel(BaseModel):
    user: str
    rating: str
    comment: str | None = None
    timestamp: Timestamp = Timestamp()


class MessageModel(BaseModel):
    user: str
    content: str
    feedback: list[FeedbackModel] | None = []
    timestamp: Timestamp = Timestamp()


class ConversationModel(BaseModel):
    id: str
    created_by: str
    participants: list[str]
    messages: list[MessageModel]
    timestamp: Timestamp = Timestamp()
