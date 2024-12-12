import os

from fai_backend.config import settings as app_settings
from fai_backend.projects.dependencies import get_project_service
from fai_backend.settings.models import SettingsDict


class SettingsService:

    @staticmethod
    async def _get_project():
        project_service = get_project_service()
        return next(iter(await project_service.read_projects(limit=1)))

    async def refresh_environment(self):
        import dotenv
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


class SettingsServiceFactory:

    @staticmethod
    def get_service() -> SettingsService:
        return SettingsService()
