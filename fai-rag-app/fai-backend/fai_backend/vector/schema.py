from pydantic import BaseModel


class VectorData(BaseModel):
    documents: list[str]
