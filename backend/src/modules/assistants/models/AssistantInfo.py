from pydantic import BaseModel


class AssistantInfo(BaseModel):
    id: str
    name: str
    description: str
    sample_questions: list[str]
    model: str
