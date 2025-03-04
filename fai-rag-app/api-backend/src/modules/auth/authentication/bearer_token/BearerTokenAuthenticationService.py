from jose import JWTError

from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity
from src.modules.auth.authentication.protocols.IAuthenticationService import IAuthenticationService
from src.modules.auth.helpers.user_jwt import verify_user_jwt


class BearerTokenAuthenticationService(IAuthenticationService):
    async def authenticate(self, payload: str) -> AuthenticatedIdentity | None:
        try:
            jwt = verify_user_jwt(payload)
        except JWTError:
            return None

        if jwt is None:
            return None

        return AuthenticatedIdentity(uid=jwt['sub'], principal_type='user')
