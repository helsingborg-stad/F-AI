from src.modules.auth.authentication.models.AuthenticationType import AuthenticationType


class AuthenticationChallengeAdapter:
    @staticmethod
    def to_challenge(authentication_method: AuthenticationType) -> str:
        mapping: dict[AuthenticationType, str] = {
            AuthenticationType.API_KEY: 'Api-Key realm="main"',
            AuthenticationType.BEARER_TOKEN: 'Bearer realm="main"',
        }
        return mapping.get(authentication_method, f'{authentication_method} realm="main"')
