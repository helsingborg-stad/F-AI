from pydantic import BaseModel


class TemplatePayload(BaseModel):
    name: str
    model: str
    instructions: str = ''
    id: str = ''
    temperature: float = 1.0
    max_tokens: int = 2500
    description: str | None = None
    sample_questions: list[str | None] | None = None
    files_collection_id: str | None = None
    response_format: str | None = None
    allow_inline_files: bool = False
    delete_label: str = "Delete"  # TODO: fix hack for allowing something to show up in list to click on.
