from fai_backend.feedback.models import FeedbackEntry
from fai_backend.feedback.providers.dummy import DummyProvider
from fai_backend.feedback.providers.github import GitHubProvider
from fai_backend.feedback.providers.protocol import IFeedbackProvider
from fai_backend.settings.service import SettingsServiceFactory, SettingKey


class FeedbackService:
    provider: IFeedbackProvider

    def __init__(self, provider: IFeedbackProvider) -> None:
        self.provider = provider

    async def send(self, data: FeedbackEntry) -> None:
        await self.provider.create_task(data)


class FeedbackServiceFactory:
    async def get_service(self):
        settings_service = SettingsServiceFactory().get_service()
        github_api_token = await settings_service.get_value(SettingKey.FEEDBACK_GITHUB_API_TOKEN)

        if github_api_token == '':
            return FeedbackService(DummyProvider())

        repo_owner = await settings_service.get_value(SettingKey.FEEDBACK_GITHUB_REPO_OWNER)
        repo_name = await settings_service.get_value(SettingKey.FEEDBACK_GITHUB_REPO_NAME)

        return FeedbackService(GitHubProvider(github_api_token, repo_owner, repo_name))
