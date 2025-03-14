from src.modules.notification.models.NotificationPayload import NotificationPayload
from src.modules.notification.protocols.INotificationService import INotificationService


class ConsoleNotificationService(INotificationService):
    async def send(self, recipient: str, payload: NotificationPayload):
        print(f'(ConsoleNotificationService) {recipient=}, {payload=}')
