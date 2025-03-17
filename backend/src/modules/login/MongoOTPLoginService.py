import os
import random

from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from src.common.hashing import hash_secret, verify_hash
from src.modules.auth.authorization.protocols.IAuthorizationService import IAuthorizationService
from src.modules.auth.helpers.user_jwt import create_user_jwt
from src.modules.login.models.ConfirmedLogin import ConfirmedLogin
from src.modules.login.models.StoredOTP import StoredOTP
from src.modules.login.protocols.ILoginService import ILoginService
from src.modules.notification.models.NotificationPayload import NotificationPayload
from src.modules.notification.protocols.INotificationService import INotificationService
from src.modules.settings.protocols.ISettingsService import ISettingsService


class MongoOTPLoginService(ILoginService):
    def __init__(
            self,
            notification_service: INotificationService,
            database: AsyncDatabase,
            authorization_service: IAuthorizationService,
            settings_service: ISettingsService
    ):
        self._notification_service = notification_service
        self._database = database
        self._authorization_service = authorization_service
        self._settings_service = settings_service

    async def initiate(self, user_id: str) -> str:
        otp = self._generate_otp(await self._settings_service.get_setting('login.fixed_otp'))
        hashed_otp = hash_secret(otp)
        stored_otp = StoredOTP(user_id=user_id, hashed_otp=hashed_otp)

        result = await self._database['login_otp'].insert_one(stored_otp.model_dump())
        await self._notification_service.send(recipient=user_id, payload=self._get_notification_payload(otp))
        return str(result.inserted_id)

    async def confirm(self, request_id: str, confirmation_code: str) -> ConfirmedLogin:
        result = await self._database['login_otp'].find_one({'_id': ObjectId(request_id)},
                                                            projection=['user_id', 'hashed_otp'])

        if not result:
            raise ValueError('Invalid request ID')

        valid_code = verify_hash(confirmation_code, result['hashed_otp'])

        if not valid_code:
            raise ValueError('Invalid confirmation code')

        await self._database['login_otp'].delete_one({'_id': ObjectId(request_id)})
        jwt = create_user_jwt(result['user_id'], {}, await self._settings_service.get_setting('jwt.user_secret'))
        return ConfirmedLogin(user_id=result['user_id'], access_token=jwt)

    @staticmethod
    def _generate_otp(fixed_otp: str | None) -> str:
        return fixed_otp if fixed_otp and len(fixed_otp) > 0 \
            else ''.join([str(random.randint(0, 9)) for _ in range(4)])

    @staticmethod
    def _get_notification_payload(otp: str) -> NotificationPayload:
        return NotificationPayload(
            subject="Your Login PIN",
            body=f"""
<html><head></head><body><p>Hello,</p><p>Login with this pin: {otp}</p></body></html>
"""
        )
