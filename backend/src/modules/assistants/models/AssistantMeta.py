from pydantic import BaseModel


class AssistantMeta(BaseModel):
    name: str
    description: str
    sample_questions: list[str]
