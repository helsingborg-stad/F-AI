from pydantic import BaseModel


class VectorSpace(BaseModel):
    name: str
