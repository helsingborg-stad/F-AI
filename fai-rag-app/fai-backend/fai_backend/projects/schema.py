from pydantic import BaseModel, EmailStr, Field, SecretStr, field_serializer

from fai_backend.assistant.models import AssistantTemplate
from fai_backend.schema import Timestamp
from fai_backend.settings.models import SettingsDict


class ProjectMember(BaseModel):
    email: EmailStr
    role: str


class ProjectRole(BaseModel):
    permissions: dict[str, bool] = Field(..., default_factory=dict)


class Project(BaseModel):
    id: str
    name: str
    type: str = 'project'
    creator: EmailStr
    description: str = ''
    timestamp: Timestamp = Timestamp()
    settings: SettingsDict = {}
    assistants: list[AssistantTemplate] = Field(default_factory=list)
    members: list[ProjectMember] = Field(..., default_factory=list)
    roles: dict[str, ProjectRole] = Field(..., default_factory=dict)
    secrets: dict[str, SecretStr] = Field(..., default_factory=dict)
    meta: dict[str, str] = Field(..., default_factory=dict)


class ProjectCreateRequest(BaseModel):
    name: str
    description: str = ''
    creator: EmailStr
    members: list[ProjectMember] = Field(..., default_factory=list)
    roles: dict[str, ProjectRole] = Field(..., default_factory=dict)
    secrets: dict[str, SecretStr] = Field(..., default_factory=dict)
    meta: dict[str, str] = Field(..., default_factory=dict)


class ProjectResponse(BaseModel):
    id: str
    name: str
    type: str
    creator: EmailStr
    description: str = ''
    timestamp: Timestamp
    assistants: list[AssistantTemplate] = Field(default_factory=list)
    members: list[ProjectMember] = Field(..., default_factory=list)
    roles: dict[str, ProjectRole] = Field(..., default_factory=dict)
    secrets: dict[str, SecretStr] = Field(..., default_factory=dict)
    meta: dict[str, str] = Field(..., default_factory=dict)

    @field_serializer('secrets', when_used='json')
    def dump_secret(self, v):
        return {k: v[k].get_secret_value() for k in v}


class ProjectUpdateRequest(ProjectResponse):
    pass
