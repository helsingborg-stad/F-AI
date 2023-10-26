from datetime import datetime
from pydantic import BaseModel, Field 


class OutputTimestamp(BaseModel):
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)