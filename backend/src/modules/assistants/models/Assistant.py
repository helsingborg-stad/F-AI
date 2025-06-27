from typing import Any

from pydantic import BaseModel


class Assistant(BaseModel):
    id: str
    owner: str
    meta: dict[str, Any]
    model: str
    llm_api_key: str | None
    instructions: str
    collection_id: str | None
    max_collection_results: int
    extra_llm_params: dict | None
