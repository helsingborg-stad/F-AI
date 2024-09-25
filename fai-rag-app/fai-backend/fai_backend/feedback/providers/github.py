import httpx

from fai_backend.feedback.models import FeedbackEntry
from fai_backend.feedback.providers.protocol import IFeedbackProvider


class GitHubProvider(IFeedbackProvider):

    def __init__(self, api_token: str, repo_owner: str, repo_name: str) -> None:
        self.api_token = api_token
        self.repo_owner = repo_owner
        self.repo_name = repo_name

    async def create_task(self, data: FeedbackEntry) -> None:
        url = f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/issues'

        headers = {
            'Authorization': f'token {self.api_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        payload = {
            'title': data.feedback_subject,
            'body': data.feedback
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
