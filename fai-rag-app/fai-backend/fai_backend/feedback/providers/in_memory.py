from fai_backend.feedback.models import FeedbackEntry
from fai_backend.feedback.providers.protocol import IFeedbackProvider


class InMemoryProvider(IFeedbackProvider):
    async def create_task(self, data: FeedbackEntry) -> None:
        print('### Feedback received ###')
        print(f'subject={data.feedback_subject}, feedback={data.feedback}')
        print('### Set GITHUB_API_TOKEN to enable creating GitHub issues ###')
