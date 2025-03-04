import uuid

from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity
from src.modules.auth.authentication.protocols.IAuthenticationService import IAuthenticationService


class ForceGuestAuthenticationService(IAuthenticationService):
    async def authenticate(self, payload: str) -> AuthenticatedIdentity | None:
        return AuthenticatedIdentity(
            principal_type='user',
            uid=f'guest_{uuid.uuid4().hex}'
        )
