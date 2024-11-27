import os
from enum import Enum

import dotenv
from pydantic import SecretStr

from fai_backend.config import Settings
from fai_backend.projects.dependencies import get_project_service
from fai_backend.settings.models import SettingsDict


class SettingKey(Enum):
    FIXED_PIN = 'FIXED_PIN'
    OPENAI_API_KEY = 'OPENAI_API_KEY'
    VLLM_CONFIG = 'VLLM_CONFIG'

    # Email
    BREVO_API_URL = 'BREVO_API_URL'
    BREVO_API_KEY = 'BREVO_API_KEY'
    MAIL_SENDER_NAME = 'MAIL_SENDER_NAME'
    MAIL_SENDER_EMAIL = 'MAIL_SENDER_EMAIL'

    # Sentry
    SENTRY_DSN = 'SENTRY_DSN'
    SENTRY_LOGGING_LEVEL = 'SENTRY_LOGGING_LEVEL'
    SENTRY_EVENT_LEVEL = 'SENTRY_EVENT_LEVEL'
    SENTRY_TRACE_SAMPLE_RATE = 'SENTRY_TRACE_SAMPLE_RATE'
    SENTRY_ENVIRONMENT = 'SENTRY_ENVIRONMENT'

    # Feedback
    FEEDBACK_GITHUB_API_TOKEN = 'FEEDBACK_GITHUB_API_TOKEN'
    FEEDBACK_GITHUB_REPO_OWNER = 'FEEDBACK_GITHUB_REPO_OWNER'
    FEEDBACK_GITHUB_REPO_NAME = 'FEEDBACK_GITHUB_REPO_NAME'


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
        str_key = str(key.value)

        if str_key in project.settings:
            return project.settings[str_key]

        defaults = Settings().model_dump()
        if str_key in defaults:
            value = defaults[str_key]
            if isinstance(value, SecretStr):
                return value.get_secret_value()
            return value

        raise KeyError(f'Unknown setting key "{str_key}"')


class SettingsServiceFactory:
    @staticmethod
    def get_service() -> SettingsService:
        return SettingsService()
