from fastapi.security import HTTPBearer
from starlette.requests import Request

from fai_backend.auth.protocol import IAuthorizationCredentials
from fai_backend.auth.schema import CustomHTTPAuthorizationCredentials


class DefaultHttpBearer(IAuthorizationCredentials):
    @staticmethod
    async def create(r: Request) -> CustomHTTPAuthorizationCredentials:
        http_auth_cred = await HTTPBearer()(r)
        return CustomHTTPAuthorizationCredentials(**http_auth_cred.model_dump(), is_disabled=False)


class NoAuth(IAuthorizationCredentials):
    @staticmethod
    async def create(r: Request) -> CustomHTTPAuthorizationCredentials:
        return CustomHTTPAuthorizationCredentials(credentials='', scheme='', is_disabled=True)


class ApiCredentialsFactory:
    @staticmethod
    def create(auth_type: str) -> IAuthorizationCredentials:
        if auth_type == 'none':
            return NoAuth()
        elif auth_type == 'http_bearer':
            return DefaultHttpBearer()
