from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field, EmailStr


class Timestamp(BaseModel):
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)


class ProjectUserRole(BaseModel):
    role: str
    project_id: str
    permissions: Dict[str, bool] = Field(..., default_factory=dict)


class User(BaseModel):
    email: EmailStr
    projects: list[ProjectUserRole] = Field(..., default_factory=list)


class ProjectUser(BaseModel):
    email: EmailStr
    role: str
    project_id: str
    permissions: Dict[str, bool] = Field(..., default_factory=dict)
