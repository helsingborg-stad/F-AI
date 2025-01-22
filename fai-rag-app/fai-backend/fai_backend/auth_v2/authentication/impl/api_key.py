from fai_backend.auth_v2.authentication.models import AuthenticatedIdentity, IAuthenticationProvider, AuthenticationType


class ApiKeyProvider(IAuthenticationProvider):
    async def validate(self, data: str | None) -> AuthenticatedIdentity | None:
        # TODO
        return AuthenticatedIdentity(
            type=AuthenticationType.API_KEY,
            uid="fai-blablabla"
        )
