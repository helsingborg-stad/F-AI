import json

from fai_backend.auth_v2.authentication.models import IAuthenticationProvider, AuthenticatedIdentity, AuthenticationType


class BearerTokenProvider(IAuthenticationProvider):
    async def validate(self, data: str | None) -> AuthenticatedIdentity | None:
        return AuthenticatedIdentity(
            type=AuthenticationType.BEARER_TOKEN,
            uid=json.loads(data)['email']
        )
