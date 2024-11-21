import os
from enum import Enum

import dotenv

from fai_backend.config import Settings
from fai_backend.projects.dependencies import get_project_service
from fai_backend.settings.models import SettingsDict


class SettingKey(Enum):
    OPENAI_API_KEY = 'OPENAI_API_KEY'


class SettingsService:
    def __init__(self):
        pass

    async def _get_project(self):
        project_service = get_project_service()
        return next(iter(await project_service.read_projects(limit=1)))

    async def refresh_environment(self):
        dotenv.load_dotenv()
        project = await self._get_project()
        for key in project.settings:
            os.environ[key] = str(project.settings[key])

    async def get_all(self) -> Settings:
        project = await self._get_project()
        defaults = Settings().model_dump()
        overrides = project.settings
        merged = defaults | overrides
        return Settings(**merged, _env_file=None)

    async def set_all(self, settings: SettingsDict):
        project = await self._get_project()
        project.settings = settings
        project_service = get_project_service()
        await project_service.update_project(project.id, project)

        for key in settings.keys():
            os.environ[key] = str(settings[key])

    async def get_value(self, key: SettingKey) -> bool | float | int | str:
        project = await self._get_project()

        if key in project.settings:
            return project.settings[key]

        defaults = Settings().model_dump()
        if key in defaults:
            return defaults[str(key)]

        raise KeyError(f'Unknown setting key "{key}"')

    async def set_value(self, key: SettingKey, value):
        project = await self._get_project()
        project.settings[key] = value
        project_service = get_project_service()
        await project_service.update_project(project.id, project)
        os.environ[str(key)] = str(value)


class SettingsServiceFactory:
    @staticmethod
    def get_service() -> SettingsService:
        return SettingsService()
