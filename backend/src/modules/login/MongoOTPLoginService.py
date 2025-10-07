import hashlib
import random
import secrets
import datetime
import time

from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.errors import DuplicateKeyError

from src.common.hashing import hash_secret, verify_hash
from src.common.mongo import ensure_expiry_index
from src.modules.auth.authorization.protocols.IAuthorizationService import IAuthorizationService
from src.modules.auth.helpers.user_jwt import create_user_jwt
from src.modules.login.models.ConfirmedLogin import ConfirmedLogin
from src.modules.login.models.StoredOTP import StoredOTP
from src.modules.login.protocols.ILoginService import ILoginService
from src.modules.metrics.models.Metric import Metric, MetricValue
from src.modules.metrics.protocols.IMetricsProvider import IMetricsProvider
from src.modules.notification.models.NotificationPayload import NotificationPayload
from src.modules.notification.protocols.INotificationService import INotificationService
from src.modules.settings.protocols.ISettingsService import ISettingsService
from src.modules.settings.settings import SettingKey


class MongoOTPLoginService(ILoginService, IMetricsProvider):
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

    async def init(self):
        otp_expire_seconds = await self._settings_service.get_setting(SettingKey.OTP_EXPIRE_SECONDS.key,
                                                                      SettingKey.OTP_EXPIRE_SECONDS.default)

        refresh_token_expire_seconds = await self._settings_service.get_setting(
            SettingKey.REFRESH_TOKEN_EXPIRE_SECONDS.key, SettingKey.REFRESH_TOKEN_EXPIRE_SECONDS.default)

        await ensure_expiry_index(self._database['login_otp'], otp_expire_seconds)
        await ensure_expiry_index(self._database['refresh_tokens'], refresh_token_expire_seconds)
        await self._database['login_metrics_logins'].create_index("uid")
        await self._database['login_metrics_logins'].create_index("timestamp")
        await self._database['login_metrics_logins'].create_index([("uid", 1), ("timestamp", 1)])

    async def initiate_login(self, user_id: str) -> str:
        otp = self._generate_otp(await self._settings_service.get_setting(SettingKey.FIXED_OTP.key))
        hashed_otp = hash_secret(otp)
        stored_otp = StoredOTP(user_id=user_id, hashed_otp=hashed_otp)

        result = await self._database['login_otp'].insert_one(
            {
                **stored_otp.model_dump(),
                'createdAt': datetime.datetime.now(datetime.UTC)
            })
        await self._notification_service.send_notification(recipient=user_id,
                                                           payload=self._get_notification_payload(otp))
        return str(result.inserted_id)

    async def confirm_login(self, request_id: str, confirmation_code: str) -> ConfirmedLogin:
        result = await self._database['login_otp'].find_one({'_id': ObjectId(request_id)},
                                                            projection=['createdAt', 'user_id', 'hashed_otp'])

        otp_creation_time = result['createdAt'] if result else None

        otp_expire_seconds = await self._settings_service.get_setting(SettingKey.OTP_EXPIRE_SECONDS.key,
                                                                      SettingKey.OTP_EXPIRE_SECONDS.default)

        if not result or (
                datetime.datetime.now(datetime.UTC).replace(
                    tzinfo=None) - otp_creation_time).total_seconds() >= otp_expire_seconds:
            raise ValueError('Invalid request ID')

        valid_code = verify_hash(confirmation_code, result['hashed_otp'])

        if not valid_code:
            raise ValueError('Invalid confirmation code')

        await self._database['login_otp'].delete_one({'_id': ObjectId(request_id)})

        user_id = result['user_id']

        return await self._create_confirmed_login(user_id)

    async def refresh_login(self, refresh_token: str) -> ConfirmedLogin:
        stored_token = await self._database['refresh_tokens'].find_one_and_delete(
            {'token': hashlib.sha1(refresh_token.encode('utf-8')).hexdigest()},
            projection=['user_id']
        )

        if not stored_token:
            raise ValueError('Invalid refresh token')

        return await self._create_confirmed_login(stored_token['user_id'])

    async def revoke_refresh_token(self, as_uid: str, refresh_token: str):
        await self._database['refresh_tokens'].delete_one({
            'token': hashlib.sha1(refresh_token.encode('utf-8')).hexdigest(),
            'user_id': as_uid
        })

    async def _create_confirmed_login(self, user_id):
        access_token_expires_at = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
            seconds=await self._settings_service.get_setting(SettingKey.JWT_EXPIRE_SECONDS.key,
                                                             SettingKey.JWT_EXPIRE_SECONDS.default))
        jwt = create_user_jwt(
            user_id,
            {},
            access_token_expires_at,
            await self._settings_service.get_setting(SettingKey.JWT_USER_SECRET.key))

        refresh_token_expire_seconds = await self._settings_service.get_setting(
            SettingKey.REFRESH_TOKEN_EXPIRE_SECONDS.key, SettingKey.REFRESH_TOKEN_EXPIRE_SECONDS.default)

        refresh_token = secrets.token_urlsafe(32)
        refresh_token_created_at = datetime.datetime.now(datetime.UTC)
        refresh_token_expires_at = refresh_token_created_at + datetime.timedelta(seconds=refresh_token_expire_seconds)

        await self._database['refresh_tokens'].insert_one({
            'token': hashlib.sha1(refresh_token.encode('utf-8')).hexdigest(),
            'user_id': user_id,
            'created_at': refresh_token_created_at
        })

        await self._analytics_track_login(user_id)

        return ConfirmedLogin(
            user_id=user_id,
            access_token=jwt,
            access_token_expires_at=access_token_expires_at,
            refresh_token=refresh_token,
            refresh_token_expires_at=refresh_token_expires_at
        )

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

    async def get_metrics(self) -> list[Metric]:
        unique_users_result = await self._database['login_metrics_logins'].aggregate([
            {"$group": {"_id": "$uid"}},
            {"$count": "total_users"}
        ])

        unique_result_list = await unique_users_result.to_list()
        unique_users_count = unique_result_list[0]['total_users'] if len(unique_result_list) > 0 else 0

        start_of_today = datetime.datetime.now(datetime.UTC).replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_today = start_of_today + datetime.timedelta(days=1)

        dau_result = await self._database['login_metrics_logins'].aggregate([
            {"$match": {"timestamp": {"$gte": start_of_today, "$lt": end_of_today}}},
            {"$group": {"_id": "$uid"}},
            {"$count": "total_users"}
        ])

        dau_result_list = await dau_result.to_list()
        dau_count = dau_result_list[0]['total_users'] if len(dau_result_list) > 0 else 0

        return [
            Metric(
                name="login_unique_users_total",
                help="Total number of unique users who have logged in",
                type="counter",
                values=[MetricValue(
                    timestamp_s=int(time.time()),
                    value=unique_users_count,
                    attributes={})]
            ),
            Metric(
                name="login_dau",
                help="DAU for today",
                type="gauge",
                values=[MetricValue(
                    timestamp_s=int(time.time()),
                    value=dau_count,
                    attributes={})]
            )
        ]

    async def _analytics_track_login(self, uid: str):
        try:
            hashed_id = hashlib.sha1(uid.encode('utf-8')).hexdigest()
            await self._database['login_metrics_logins'].insert_one({
                "_id": ObjectId(),
                "uid": hashed_id,
                "timestamp": datetime.datetime.now(datetime.UTC)
            })
        except DuplicateKeyError:
            pass
        except Exception as e:
            print(e)
