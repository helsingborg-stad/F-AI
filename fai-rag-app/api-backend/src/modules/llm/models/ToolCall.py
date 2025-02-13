from typing import Literal

from pydantic import BaseModel

from src.modules.llm.models import ToolCallFunction


class ToolCall(BaseModel):
    id: str
    type: Literal["function"]
    function: ToolCallFunction
