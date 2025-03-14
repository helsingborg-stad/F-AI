from pydantic import BaseModel


class ToolCallFunction(BaseModel):
    name: str
    arguments: str
