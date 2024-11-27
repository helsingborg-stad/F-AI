from typing import Dict

from pydantic import BaseModel

SettingsDict = Dict[str, bool | float | int | str]


class Config(BaseModel):
    config: SettingsDict
