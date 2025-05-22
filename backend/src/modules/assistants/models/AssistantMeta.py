from pydantic import BaseModel


class AssistantMeta(BaseModel):
    name: str
    description: str
    avatar_base64: str | None
    primary_color: str
    allow_files: bool
    sample_questions: list[str]
    is_public: bool
