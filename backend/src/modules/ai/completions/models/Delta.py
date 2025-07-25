from pydantic import BaseModel


class Delta(BaseModel):
    role: str
    content: str | None = None
    reasoning_content: str | None = None
