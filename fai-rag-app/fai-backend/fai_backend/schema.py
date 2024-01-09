from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class Timestamp(BaseModel):
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)


class ProjectUserRole(BaseModel):
    role: str
    project_id: str
    permissions: dict[str, bool] = Field(..., default_factory=dict)


class User(BaseModel):
    email: EmailStr
    projects: list[ProjectUserRole] = Field(..., default_factory=list)


class ProjectUser(BaseModel):
    email: EmailStr
    role: str
    project_id: str
    permissions: dict[str, bool] = Field(..., default_factory=dict)
