from typing import Literal

from pydantic import BaseModel, Field, computed_field

from conversations.models import Message
from utils import try_get_first_match


class QuestionEntry(BaseModel):
    id: str
    messages: list[Message] = Field(default_factory=list, repr=False)
    metadata: dict = Field(default_factory=dict, repr=False)

    @computed_field
    def subject(self) -> str:
        return self.metadata['subject']

    @computed_field
    def errand_id(self) -> str:
        return self.metadata['errand_id']

    @computed_field
    def status(self) -> Literal['open', 'pending', 'answered', 'resolved', 'closed']:
        if try_get_first_match(
                self.messages,
                lambda message: message.type == 'event' and message.content == 'user_closed_question'
        ):
            return 'closed'
        elif len(self.messages) == 1:
            return 'open'
        elif (
                self.answer is not None
                and self.answer.type == 'answer'
                or self.answer
                and self.answer.type == 'generated_answer'
                and len(self.answer.feedback) > 1):
            return 'resolved'
        elif len(self.messages) > 1 and self.answer is None:
            return 'pending'

    @computed_field
    def review_status(self) -> Literal['approved', 'rejected'] | None:
        answer = try_get_first_match(
            self.messages,
            lambda message: message.type == 'generated_answer'
                            and len(message.feedback) > 0
        )

        if answer is not None:
            return 'approved' if answer.feedback[0].rating == 'approved' else 'rejected'

        return None

    @computed_field
    def answer(self) -> Message | None:
        answer = try_get_first_match(
            self.messages,
            lambda message: message.type == 'answer' or
                            message.type == 'generated_answer'
                            and len(message.feedback) > 0
                            and message.feedback[0].rating == 'approved'
        )
        return answer if answer is not None else None


class QuestionDetails(QuestionEntry):
    @computed_field
    def question(self) -> Message:
        return self.messages[0]


class SubmitQuestionPayload(BaseModel):
    subject: str
    question: str
    errand_id: str


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
