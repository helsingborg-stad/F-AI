from pydantic import BaseModel


class Model(BaseModel):
    key: str
    provider: str
    display_name: str
    description: str
