from src.modules.notification.ConsoleNotificationService import ConsoleNotificationService
from src.modules.notification.protocols.INotificationService import INotificationService


class NotificationServiceFactory:
    def get(self) -> INotificationService:
        return ConsoleNotificationService()
