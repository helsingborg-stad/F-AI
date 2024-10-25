from pydantic import BaseModel


class FeedbackEntry(BaseModel):
    feedback_subject: str
    feedback: str
