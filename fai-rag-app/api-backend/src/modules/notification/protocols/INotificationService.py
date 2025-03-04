from typing import Protocol


class INotificationService(Protocol):
    async def send(self, recipient: str, payload: str):
        ...
