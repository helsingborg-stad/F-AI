import nltk
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.routing import APIRoute
from motor.motor_asyncio import AsyncIOMotorClient

from fai_backend.assistant.models import AssistantChatHistoryModel, StoredQuestionModel
from fai_backend.collection.models import CollectionMetadataModel
from fai_backend.config import settings
from fai_backend.projects.schema import ProjectMember, ProjectRole
from fai_backend.repositories import ConversationDocument, PinCodeModel, ProjectModel, projects_repo
from fai_backend.sentry.watcher import Watcher
from fai_backend.settings.service import SettingsServiceFactory, SettingKey


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
                'can_edit_settings',
                'can_edit_project_users',
                'can_edit_project_roles',
                'can_edit_project_secrets',
                'can_ask_questions',
                'can_review_answers',
                'can_edit_questions_and_answers',
                'can_upload_document',
                'can_edit_assistant',
            ]
            return {
                x: y
                for x, y in zip(
                    permissions,
                    [value] * len(permissions),
                )
            }

        initial_project = await projects_repo.create(
            ProjectModel(
                name='Project',
                creator=settings.APP_ADMIN_EMAIL,
                assistants=[],
                members=[
                    ProjectMember(
                        email=settings.APP_ADMIN_EMAIL,
                        role='admin'
                    )
                ],
                roles={
                    'basic': ProjectRole(permissions={'can_ask_questions': True}),
                    'admin': ProjectRole(permissions=create_permissions(True)),
                    'manager': ProjectRole(permissions=create_permissions(False)),
                    'reviewer': ProjectRole(permissions=create_permissions(False)),
                    'tester': ProjectRole(permissions=create_permissions(False))
                },
                secrets={'openai_api_key': 'sk-123'},
                meta={},
                settings={}
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
        document_models=[
            ProjectModel,
            PinCodeModel,
            ConversationDocument,
            AssistantChatHistoryModel,
            CollectionMetadataModel,
            StoredQuestionModel
        ]
    )


async def setup_sentry():
    settings_service = SettingsServiceFactory().get_service()
    dsn = await settings_service.get_value(SettingKey.SENTRY_DSN)

    if len(dsn) == 0:
        return

    sentry_logger = Watcher(
        dsn=dsn,
        environment=await settings_service.get_value(SettingKey.SENTRY_ENVIRONMENT),
        level=await settings_service.get_value(SettingKey.SENTRY_LOGGING_LEVEL),
        event_level=await settings_service.get_value(SettingKey.SENTRY_EVENT_LEVEL),
        trace_sample_rate=await settings_service.get_value(SettingKey.SENTRY_TRACE_SAMPLE_RATE)
    )

    sentry_logger.initialize()


async def setup_file_parser():
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger_eng')


async def setup_settings():
    service = SettingsServiceFactory().get_service()
    await service.refresh_environment()
