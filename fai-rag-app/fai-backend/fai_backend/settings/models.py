from typing import Dict

from pydantic import BaseModel

SettingsDict = Dict[str, bool | float | int | str]  # Note: order of types is important!


class Config(BaseModel):
    config: SettingsDict
