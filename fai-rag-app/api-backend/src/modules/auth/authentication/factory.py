import os
from collections.abc import Callable

from src.modules.auth.authentication.ForceGuestAuthenticationService import ForceGuestAuthenticationService
from src.modules.auth.authentication.models.AuthenticationType import AuthenticationType
from src.modules.auth.authentication.protocols.IAuthenticationService import IAuthenticationService


class AuthenticationServiceFactory:
    def __init__(self, auth_map: dict[AuthenticationType, Callable[[], IAuthenticationService]]):
        self.auth_map = auth_map

    def get(self, auth_type: AuthenticationType) -> IAuthenticationService:
        if os.environ['DISABLE_AUTH'] == '1':
            return ForceGuestAuthenticationService()

        if auth_type in self.auth_map:
            return self.auth_map[auth_type]()
        raise ValueError(f"Authentication type '{auth_type}' not supported")
