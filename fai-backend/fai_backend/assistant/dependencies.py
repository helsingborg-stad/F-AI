from fastapi import Depends

from fai_backend.assistant.service import AssistantTemplateStore
from fai_backend.projects.dependencies import get_project_service
from fai_backend.projects.service import ProjectService


def get_template_service(project_service: ProjectService = Depends(get_project_service)) -> 'AssistantTemplateStore':
    return AssistantTemplateStore(project_service=project_service)
