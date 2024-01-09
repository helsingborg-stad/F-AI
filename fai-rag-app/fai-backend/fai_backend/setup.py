from beanie import init_beanie
from fastapi import FastAPI
from fastapi.routing import APIRoute
from motor.motor_asyncio import AsyncIOMotorClient

from fai_backend.config import settings
from fai_backend.repositories import (
    ConversationDocument,
    PinCodeModel,
    ProjectModel,
    projects_repo,
)


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
        permissions = [
            'can_edit_project_users',
            'can_edit_project_roles',
            'can_edit_project_secrets',
            'can_ask_questions',
            'can_review_answers',
            'can_edit_questions_and_answers',
        ]

        def create_permissions(permissions_list: list[str], value: bool = False):
            return {
                x: y
                for x, y in zip(
                    permissions,
                    [value] * len(permissions_list),
                )
            }

        initial_project = await projects_repo.create(
            ProjectModel.model_validate(
                {
                    'name': settings.APP_PROJECT_NAME,
                    'creator': settings.APP_ADMIN_EMAIL,
                    'description': 'Initial project created on startup',
                    'members': [{'email': settings.APP_ADMIN_EMAIL, 'role': 'admin'}],
                    'roles': {
                        'admin': {'permissions': create_permissions(permissions, True)},
                        'manager': {
                            'permissions': create_permissions(permissions, False)
                        },
                        'reviewer': {
                            'permissions': create_permissions(permissions, False)
                        },
                        'tester': {
                            'permissions': create_permissions(permissions, False)
                        },
                    },
                    'secrets': {'openai_api_key': 'sk-123'},
                    'meta': {},
                }
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
