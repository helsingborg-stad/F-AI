import os

import pytest_asyncio
import pytest
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from fai_backend.config import Settings
from fai_backend.projects.schema import Project, ProjectCreateRequest
from fai_backend.projects.service import ProjectService
from fai_backend.repositories import ProjectModel, ProjectRepository
from fai_backend.repository.mongodb import MongoDBRepo
from fai_backend.settings.service import SettingsService


@pytest_asyncio.fixture
async def project_repo() -> ProjectRepository:
    await init_beanie(database=AsyncMongoMockClient().test_db, document_models=[ProjectModel])
    yield MongoDBRepo[Project, ProjectModel](Project, ProjectModel)
    await ProjectModel.get_motor_collection().drop()


@pytest_asyncio.fixture
async def project_service(project_repo) -> ProjectService:
    return ProjectService(project_repo)


@pytest_asyncio.fixture
async def settings_service(project_service):
    await project_service.create_project(ProjectCreateRequest(
        name='test_project',
        creator='mail@example.com'))
    return SettingsService(project_service)


@pytest.fixture
def app_settings():
    os.environ.clear()
    return Settings()


def test_reload_settings_from_env(settings_service, app_settings):
    os.environ['FIXED_PIN'] = '1234'
    app_settings.reload_from_env()

    assert app_settings.MONGO_DB_NAME == 'fai-rag-app'
    assert app_settings.MONGO_DB_URI == 'mongodb://localhost:27017'
    assert app_settings.FIXED_PIN == '1234'


@pytest.mark.asyncio
async def test_get_settings(settings_service, app_settings):
    os.environ['FIXED_PIN'] = '4321'
    app_settings.reload_from_env()
    settings = await settings_service.get_all(app_settings)

    assert settings['FIXED_PIN'] == '4321'
    assert settings['MONGO_DB_NAME'] == 'fai-rag-app'
    assert settings['MONGO_DB_URI'] == 'mongodb://localhost:27017'


@pytest.mark.asyncio
async def test_update_settings(settings_service, app_settings):
    await settings_service.set_all({'FIXED_PIN': '1111'}, app_settings)

    assert app_settings.FIXED_PIN == '1111'


@pytest.mark.asyncio
async def test_setup_settings(settings_service, app_settings):
    os.environ['FIXED_PIN'] = '1234'
    await settings_service.reload_envs_from_settings_repo()
    app_settings.reload_from_env()

    assert app_settings.FIXED_PIN == '1234'
