from typing import Callable

from fai_backend.auth_v2.authentication.impl.api_key import ApiKeyProvider
from fai_backend.auth_v2.authentication.impl.bearer_token import BearerTokenProvider
from fai_backend.auth_v2.authentication.models import IAuthenticationProvider, AuthenticationType


class AuthenticationFactory:
    @staticmethod
    async def get(auth_type: str) -> IAuthenticationProvider:
        mapping: dict[str, Callable[[], IAuthenticationProvider]] = {
            AuthenticationType.API_KEY: ApiKeyProvider,
            AuthenticationType.BEARER_TOKEN: BearerTokenProvider,
        }
        if auth_type in mapping:
            return mapping[auth_type]()
        raise ValueError(f"Authentication type '{auth_type}' not supported")
