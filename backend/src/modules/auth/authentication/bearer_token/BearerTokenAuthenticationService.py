from jose import JWTError

from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity
from src.modules.auth.authentication.protocols.IAuthenticationService import IAuthenticationService
from src.modules.auth.helpers.user_jwt import verify_user_jwt
from src.modules.settings.protocols.ISettingsService import ISettingsService
from src.modules.settings.settings import SettingKey


class BearerTokenAuthenticationService(IAuthenticationService):
    def __init__(self, settings_service: ISettingsService):
        self._settings_service = settings_service

    async def authenticate(self, payload: str) -> AuthenticatedIdentity | None:
        try:
            jwt = verify_user_jwt(payload, await self._settings_service.get_setting(SettingKey.JWT_USER_SECRET.key))
        except JWTError:
            return None

        if jwt is None:
            return None

        return AuthenticatedIdentity(uid=jwt['sub'])
