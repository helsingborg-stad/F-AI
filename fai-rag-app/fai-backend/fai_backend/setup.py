import json
import os

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.routing import APIRoute
from motor.motor_asyncio import AsyncIOMotorClient

from fai_backend.config import settings
from fai_backend.projects.schema import ProjectMember, ProjectRole
from fai_backend.repositories import ConversationDocument, PinCodeModel, ProjectModel, projects_repo
from fai_backend.assistant.models import AssistantTemplate, LLMStreamSettings, LLMStreamDef, LLMStreamMessage


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'

    return None


async def setup_project():
    projects = await projects_repo.list()
    if not projects or len(projects) == 0:
        def create_permissions(value: bool):
            permissions = [
                'can_edit_project_users',
                'can_edit_project_roles',
                'can_edit_project_secrets',
                'can_ask_questions',
                'can_review_answers',
                'can_edit_questions_and_answers',
            ]
            return {
                x: y
                for x, y in zip(
                    permissions,
                    [value] * len(permissions),
                )
            }

        assistant_templates_dir = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                '../../../data/assistant-templates'))
        initial_assistants = \
            [
                AssistantTemplate(**json.loads(open(os.path.join(assistant_templates_dir, f)).read()))
                for f in os.listdir(assistant_templates_dir)
                if f.endswith('.json')
            ] if os.path.exists(assistant_templates_dir) else []

        initial_project = await projects_repo.create(
            ProjectModel(
                name='Project',
                creator=settings.APP_ADMIN_EMAIL,
                assistants=initial_assistants,
                members=[
                    ProjectMember(
                        email=settings.APP_ADMIN_EMAIL,
                        role='admin'
                    )
                ],
                roles={
                    'admin': ProjectRole(permissions=create_permissions(True)),
                    'manager': ProjectRole(permissions=create_permissions(False)),
                    'reviewer': ProjectRole(permissions=create_permissions(False)),
                    'tester': ProjectRole(permissions=create_permissions(False))
                },
                secrets={'openai_api_key': 'sk-123'},
                meta={}
            )
        )

        if initial_project:
            print('Initialized Initial Project')
        else:
            raise Exception('Failed to create initial project')


async def setup_db():
    client = AsyncIOMotorClient(settings.MONGO_DB_URI)
    await init_beanie(
        database=client[settings.MONGO_DB_NAME],
        document_models=[ProjectModel, PinCodeModel, ConversationDocument],
    )
