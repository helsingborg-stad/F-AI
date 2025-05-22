from pydantic import BaseModel


class AssistantInfo(BaseModel):
    id: str
    name: str
    description: str
    avatar_base64: str | None
    primary_color: str
    sample_questions: list[str]
    model: str
