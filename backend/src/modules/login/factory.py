from pymongo.asynchronous.database import AsyncDatabase

from src.modules.auth.authorization.protocols.IAuthorizationService import IAuthorizationService
from src.modules.login.MongoOTPLoginService import MongoOTPLoginService
from src.modules.login.protocols.ILoginService import ILoginService
from src.modules.notification.protocols.INotificationService import INotificationService
from src.modules.settings.protocols.ISettingsService import ISettingsService


class LoginServiceFactory:
    def __init__(
            self,
            mongo_database: AsyncDatabase,
            authorization_service: IAuthorizationService,
            notification_service: INotificationService,
            settings_service: ISettingsService
    ):
        self._mongo_database = mongo_database
        self._authorization_service = authorization_service
        self._notification_service = notification_service
        self._settings_service = settings_service

    async def get(self) -> ILoginService:
        service = MongoOTPLoginService(
            notification_service=self._notification_service,
            database=self._mongo_database,
            authorization_service=self._authorization_service,
            settings_service=self._settings_service
        )
        await service.init()
        return service
