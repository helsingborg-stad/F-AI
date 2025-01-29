import os
import dotenv

from fai_backend.config import Settings
from fai_backend.projects.service import ProjectService
from fai_backend.settings.models import SettingsDict


class SettingsService:

    def __init__(self, project_service: ProjectService) -> None:
        self.project_service = project_service

    async def _get_project(self):
        return next(iter(await self.project_service.read_projects(limit=1)))

    async def reload_envs_from_settings_repo(self):
        dotenv.load_dotenv()
        project = await self._get_project()

        for key, value in project.settings.items():
            os.environ[key] = str(value)

    async def get_all(self, app_settings: Settings) -> SettingsDict:
        project = await self._get_project()
        defaults = app_settings.model_dump()
        overrides = project.settings
        merged = defaults | overrides
        return merged

    async def set_all(self, settings: SettingsDict, app_settings: Settings):
        project = await self._get_project()
        project.settings = settings
        await self.project_service.update_project(project.id, project)
        await self.reload_envs_from_settings_repo()
        app_settings.reload_from_env()


class SettingsServiceFactory:

    @staticmethod
    def get_service(project_service: ProjectService) -> SettingsService:
        return SettingsService(project_service)
