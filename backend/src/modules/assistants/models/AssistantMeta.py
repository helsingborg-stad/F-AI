from pydantic import BaseModel


class AssistantMeta(BaseModel):
    name: str
    description: str
    allow_files: bool
    sample_questions: list[str]
    is_public: bool
