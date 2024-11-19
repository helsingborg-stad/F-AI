from pydantic import BaseModel


class Config(BaseModel):
    config: dict[str, bool | float | int | str]  # Note: order of types is important!
