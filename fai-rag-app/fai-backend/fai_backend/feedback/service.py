from fai_backend.config import Settings, settings
from fai_backend.feedback.models import FeedbackEntry
from fai_backend.feedback.providers.github import GitHubProvider
from fai_backend.feedback.providers.in_memory import InMemoryProvider
from fai_backend.feedback.providers.protocol import IFeedbackProvider


class FeedbackService:
    provider: IFeedbackProvider

    def __init__(self, provider: IFeedbackProvider) -> None:
        self.provider = provider

    async def send(self, data: FeedbackEntry) -> None:
        await self.provider.create_task(data)


def create_feedback_provider(feedback_settings: Settings) -> IFeedbackProvider:
    api_token = feedback_settings.FEEDBACK_GITHUB_API_TOKEN.get_secret_value()
    repo_owner = feedback_settings.FEEDBACK_GITHUB_REPO_OWNER
    repo_name = feedback_settings.FEEDBACK_GITHUB_REPO_NAME

    if api_token == '':
        return InMemoryProvider()

    return GitHubProvider(api_token, repo_owner, repo_name)


feedback_provider = create_feedback_provider(settings)


def get_feedback_service() -> FeedbackService:
    return FeedbackService(feedback_provider)
