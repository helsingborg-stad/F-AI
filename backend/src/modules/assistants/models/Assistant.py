from pydantic import BaseModel

from src.modules.assistants.models.AssistantMeta import AssistantMeta


class Assistant(BaseModel):
    id: str
    owner: str
    meta: AssistantMeta
    model: str
    llm_api_key: str | None
    instructions: str
    collection_id: str | None
    max_collection_results: int
    response_schema: dict[str, object] | None = None
    extra_llm_params: dict[str, float | int | bool | str] | None
