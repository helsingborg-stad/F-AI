from typing import Literal

from pydantic import BaseModel, Field

from fai_backend.conversations.schema import ResponseMessage
from fai_backend.schema import Timestamp


class QuestionEntry(BaseModel):
    id: str
    type: str
    messages: list[ResponseMessage] = Field(default_factory=list, repr=False)
    metadata: dict = Field(default_factory=dict, repr=False)
    tags: list[str] = Field(default_factory=list)
    subject: str
    errand_id: str
    status: Literal['open', 'pending', 'answered', 'resolved', 'closed'] | None
    review_status: Literal['approved', 'rejected', 'in-progress', 'closed', 'blocked', 'open'] | None
    answer: ResponseMessage | None
    timestamp: Timestamp


class QuestionDetails(QuestionEntry):
    question: ResponseMessage


class SubmitQuestionPayload(BaseModel):
    subject: str
    question: str
    errand_id: str
    tags: list[str]


class SubmitAnswerPayload(BaseModel):
    question_id: str
    answer: str


class GenerateAnswerPayload(BaseModel):
    question_id: str
    answer: str


class ApproveAnswerPayload(BaseModel):
    question_id: str
    rating: Literal['approved']
    comment: str | None = Field(default=None)


class RejectAnswerPayload(BaseModel):
    question_id: str
    rating: Literal['rejected']
    comment: str = Field(default=None)


FeedbackPayload = ApproveAnswerPayload | RejectAnswerPayload


class QuestionFilterParams(BaseModel):
    q: str | None = None
    tags: list[str] | None = None
    status: str | None = None
    review_status: str | None = None
    sort: str | None = None
    sort_order: str | None = None
