from typing import List, Dict

from pydantic import BaseModel, Field, EmailStr, SecretStr, field_serializer

from fai_backend.schema import Timestamp


class ProjectMember(BaseModel):
    email: EmailStr
    role: str


class ProjectRole(BaseModel):
    permissions: Dict[str, bool] = Field(..., default_factory=dict)


class Project(BaseModel):
    id: str
    name: str
    type: str = "project"
    creator: EmailStr
    description: str = ""
    timestamp: Timestamp = Timestamp()
    members: List[ProjectMember] = Field(..., default_factory=list)
    roles: Dict[str, ProjectRole] = Field(..., default_factory=dict)
    secrets: Dict[str, SecretStr] = Field(..., default_factory=dict)
    meta: Dict[str, str] = Field(..., default_factory=dict)


class ProjectCreateRequest(BaseModel):
    name: str
    description: str = ""
    creator: EmailStr
    members: List[ProjectMember] = Field(..., default_factory=list)
    roles: Dict[str, ProjectRole] = Field(..., default_factory=dict)
    secrets: Dict[str, SecretStr] = Field(..., default_factory=dict)
    meta: Dict[str, str] = Field(..., default_factory=dict)


class ProjectResponse(BaseModel):
    id: str
    name: str
    type: str
    creator: EmailStr
    description: str = ""
    timestamp: Timestamp
    members: List[ProjectMember] = Field(..., default_factory=list)
    roles: Dict[str, ProjectRole] = Field(..., default_factory=dict)
    secrets: Dict[str, SecretStr] = Field(..., default_factory=dict)
    meta: Dict[str, str] = Field(..., default_factory=dict)

    @field_serializer("secrets", when_used="json")
    def dump_secret(self, v):
        return {k: v[k].get_secret_value() for k in v}


class ProjectUpdateRequest(ProjectResponse):
    pass
