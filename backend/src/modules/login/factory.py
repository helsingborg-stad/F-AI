from pymongo.asynchronous.database import AsyncDatabase

from src.modules.auth.authorization.protocols.IAuthorizationService import IAuthorizationService
from src.modules.login.MongoOTPLoginService import MongoOTPLoginService
from src.modules.login.protocols.ILoginService import ILoginService
from src.modules.notification.protocols.INotificationService import INotificationService


class LoginServiceFactory:
    def __init__(
            self,
            mongo_database: AsyncDatabase,
            authorization_service: IAuthorizationService,
            notification_service: INotificationService
    ):
        self._mongo_database = mongo_database
        self._authorization_service = authorization_service
        self._notification_service = notification_service

    def get(self) -> ILoginService:
        return MongoOTPLoginService(
            notification_service=self._notification_service,
            database=self._mongo_database,
            authorization_service=self._authorization_service,
        )
