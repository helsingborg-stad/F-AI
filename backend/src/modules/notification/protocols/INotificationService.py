from typing import Protocol

from src.modules.notification.models.NotificationPayload import NotificationPayload


class INotificationService(Protocol):
    async def send_notification(self, recipient: str, payload: NotificationPayload):
        ...
