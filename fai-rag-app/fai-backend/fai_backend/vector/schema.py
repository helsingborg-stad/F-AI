from pydantic import BaseModel


class VectorData(BaseModel):
    artifacts: list[str]
