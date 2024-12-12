import os
from enum import Enum

import dotenv
from pydantic import SecretStr

from fai_backend.config import settings as app_settings
from fai_backend.projects.dependencies import get_project_service
from fai_backend.settings.models import SettingsDict


class SettingKey(Enum):
    FIXED_PIN = 'FIXED_PIN'
    OPENAI_API_KEY = 'OPENAI_API_KEY'
    BREVO_API_URL = 'BREVO_API_URL'
    BREVO_API_KEY = 'BREVO_API_KEY'


class SettingsService:
    def __init__(self):
        pass

    async def _get_project(self):
        project_service = get_project_service()
        return next(iter(await project_service.read_projects(limit=1)))

    async def refresh_environment(self):
        dotenv.load_dotenv()
        project = await self._get_project()

        for key, value in project.settings.items():
            os.environ[key] = str(value)

        app_settings.reload_from_env()

    async def get_all(self) -> SettingsDict:
        project = await self._get_project()
        defaults = app_settings.model_dump()
        overrides = project.settings
        merged = defaults | overrides
        return app_settings.model_validate(merged)

    async def set_all(self, settings: SettingsDict):
        project = await self._get_project()
        project.settings = settings
        project_service = get_project_service()
        await project_service.update_project(project.id, project)

        for key, value in settings.items():
            os.environ[key] = str(value)

        app_settings.reload_from_env()

    async def get_value(self, key: SettingKey) -> bool | float | int | str:
        project = await self._get_project()
        str_key = str(key.value)

        if str_key in project.settings:
            return project.settings[str_key]

        defaults = app_settings.model_dump()
        if str_key in defaults:
            value = defaults[str_key]
            if isinstance(value, SecretStr):
                return value.get_secret_value()
            return value

        raise KeyError(f'Unknown setting key "{str_key}"')

    async def set_value(self, key: SettingKey, value):
        project = await self._get_project()
        project.settings[key.value] = value
        project_service = get_project_service()
        await project_service.update_project(project.id, project)
        os.environ[str(key.value)] = str(value)


class SettingsServiceFactory:
    @staticmethod
    def get_service() -> SettingsService:
        return SettingsService()
