from pydantic import BaseModel

from src.modules.assistants.models.AssistantMeta import AssistantMeta


class Assistant(BaseModel):
    id: str
    owner: str
    meta: AssistantMeta
    model: str
    llm_api_key: str | None
    instructions: str
    temperature: float
    max_tokens: int
    collection_id: str | None
