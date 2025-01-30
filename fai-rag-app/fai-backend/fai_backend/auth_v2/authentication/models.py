from typing import Protocol

from pydantic import BaseModel


class AuthenticationType:
    NONE = 'NONE'
    API_KEY = 'api_key'
    BEARER_TOKEN = 'bearer_token'


class AuthenticatedIdentity(BaseModel):
    uid: str


class IAuthenticationProvider(Protocol):
    async def validate(self, data: str | None) -> AuthenticatedIdentity | None:
        ...
