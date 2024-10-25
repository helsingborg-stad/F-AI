from typing import Protocol

from fai_backend.feedback.models import FeedbackEntry


class IFeedbackProvider(Protocol):
    async def create_task(self, data: FeedbackEntry):
        ...
