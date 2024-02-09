from pydantic import BaseModel


class QuestionResponse(BaseModel):
    id: str
    question: str
    created_by: str
    subject: str
    errand_id: str
    answer: str | None = None


class SubmitQuestionRequest(BaseModel):
    subject: str
    question: str
    errand_id: str
