from pydantic import BaseModel


class TemplatePayload(BaseModel):
    name: str
    model: str
    instructions: str = ''
    id: str = ''
    temperature: float = 1.0
    description: str | None = None
    sample_questions: list[str] | None = None
    files_collection_id: str | None = None