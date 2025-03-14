import os

from src.modules.api_key.protocols.IApiKeyService import IApiKeyService
from src.modules.auth.authentication.ForceGuestAuthenticationService import ForceGuestAuthenticationService
from src.modules.auth.authentication.api_key.ApiKeyAuthenticationService import ApiKeyAuthenticationService
from src.modules.auth.authentication.bearer_token.BearerTokenAuthenticationService import \
    BearerTokenAuthenticationService
from src.modules.auth.authentication.cookie_token.CookieTokenAuthenticationService import \
    CookieTokenAuthenticationService
from src.modules.auth.authentication.models.AuthenticationType import AuthenticationType
from src.modules.auth.authentication.protocols.IAuthenticationService import IAuthenticationService
from src.modules.settings.protocols.ISettingsService import ISettingsService


class AuthenticationServiceFactory:
    def __init__(
            self,
            supported_auth_methods: list[AuthenticationType],
            api_key_service: IApiKeyService,
            settings_service: ISettingsService
    ):
        self._supported_auth_methods = supported_auth_methods
        self._api_key_service = api_key_service
        self._settings_service = settings_service

    def get(self, auth_type: AuthenticationType) -> IAuthenticationService:
        if auth_type not in self._supported_auth_methods:
            raise ValueError(f'Authentication method {auth_type} not supported')

        auth_method = AuthenticationType.GUEST if os.environ['DISABLE_AUTH'] == '1' else auth_type

        match auth_method:
            case AuthenticationType.GUEST:
                return ForceGuestAuthenticationService()
            case AuthenticationType.API_KEY:
                return ApiKeyAuthenticationService(api_key_service=self._api_key_service)
            case AuthenticationType.BEARER_TOKEN:
                return BearerTokenAuthenticationService(self._settings_service)
            case AuthenticationType.COOKIE_TOKEN:
                return CookieTokenAuthenticationService(self._settings_service)

        raise ValueError(f"Authentication method '{auth_type}' not implemented")
