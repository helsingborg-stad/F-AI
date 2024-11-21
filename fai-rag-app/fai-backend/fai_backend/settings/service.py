from enum import Enum

from fai_backend.config import Settings
from fai_backend.projects.dependencies import get_project_service
from fai_backend.settings.models import SettingsDict


class SettingKey(Enum):
    OPENAI_API_KEY = 'OPENAI_API_KEY'


class SettingsService:
    def __init__(self):
        pass

    async def get_all(self) -> Settings:
        project_service = get_project_service()
        project = next(iter(await project_service.read_projects(limit=1)))
        defaults = Settings().model_dump()
        overrides = project.settings
        merged = defaults | overrides
        return Settings(**merged, _env_file=None)

    async def set_all(self, settings: SettingsDict):
        project_service = get_project_service()
        project = next(iter(await project_service.read_projects(limit=1)))
        project.settings = settings
        await project_service.update_project(project.id, project)

    async def get_value(self, key: SettingKey) -> bool | float | int | str:
        project_service = get_project_service()
        project = next(iter(await project_service.read_projects(limit=1)))

        if key in project.settings:
            return project.settings[key]

        defaults = Settings().model_dump()
        if key in defaults:
            return defaults[str(key)]

        raise KeyError(f'Unknown setting key "{key}"')

    async def set_value(self, key: SettingKey, value):
        project_service = get_project_service()
        project = next(iter(await project_service.read_projects(limit=1)))
        project.settings[key] = value
        await project_service.update_project(project.id, project)


class SettingsServiceFactory:
    @staticmethod
    def get_service() -> SettingsService:
        return SettingsService()
