import os

from src.modules.notification.BrevoEmailNotificationService import BrevoEmailNotificationService
from src.modules.notification.ConsoleNotificationService import ConsoleNotificationService
from src.modules.notification.SmtpNotificationService import SmtpNotificationService
from src.modules.notification.protocols.INotificationService import INotificationService
from src.modules.settings.protocols.ISettingsService import ISettingsService


class NotificationServiceFactory:
    def __init__(self, settings_service: ISettingsService):
        self._settings_service = settings_service

    def get(self) -> INotificationService:
        method = os.environ["NOTIFICATION_METHOD"]

        match method:
            case "console":
                return ConsoleNotificationService()
            case "brevo":
                return BrevoEmailNotificationService(self._settings_service)
            case "smtp":
                return SmtpNotificationService(self._settings_service)

        raise Exception(f"Invalid notification method {method}")
