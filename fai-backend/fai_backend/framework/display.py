import enum
from typing import Literal

from pydantic import BaseModel


class DisplayAs(str, enum.Enum):
    auto = 'auto'
    link = 'link'
    date = 'date'


class DisplayField(BaseModel):
    type: Literal['DisplayField'] = 'DisplayField'
    key: str
    label: str = ''
    id: str | None = None
    display: DisplayAs = DisplayAs.auto
