from datetime import datetime, timezone
from typing import Literal, Any
from pydantic import BaseModel, Field


def _epoch_datetime() -> datetime:
    """Return Unix epoch as datetime (1970-01-01 00:00:00 UTC)."""
    return datetime.fromtimestamp(0, tz=timezone.utc)


class Model(BaseModel):
    key: str = Field(..., min_length=1, pattern=r'^[a-zA-Z0-9._/-]+$')
    provider: str = Field(..., min_length=1)
    display_name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    meta: dict[str, Any] = Field(default_factory=dict)
    
    created_at: datetime = Field(default_factory=_epoch_datetime)
    updated_at: datetime = Field(default_factory=_epoch_datetime)
    status: Literal['active', 'deprecated', 'disabled'] = 'active'
    visibility: Literal['public', 'internal'] = 'public'
    version: int = 1
