from pydantic import BaseModel


class Group(BaseModel):
    id: str
    owner: str
    label: str
    members: list[str]
    scopes: list[str]
