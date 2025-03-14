import os

from src.modules.notification.BrevoEmailNotificationService import BrevoEmailNotificationService
from src.modules.notification.ConsoleNotificationService import ConsoleNotificationService
from src.modules.notification.protocols.INotificationService import INotificationService


class NotificationServiceFactory:
    def get(self) -> INotificationService:
        method = os.environ["NOTIFICATION_METHOD"]

        match method:
            case "console":
                return ConsoleNotificationService()
            case "brevo":
                return BrevoEmailNotificationService()

        raise Exception(f"Invalid notification method {method}")
