from typing import Protocol

from starlette.requests import Request

from fai_backend.auth.schema import CustomHTTPAuthorizationCredentials


class IAuthorizationCredentials(Protocol):
    @staticmethod
    async def create(r: Request) -> CustomHTTPAuthorizationCredentials:
        ...
