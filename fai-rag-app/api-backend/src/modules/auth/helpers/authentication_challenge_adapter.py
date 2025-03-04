from src.modules.auth.authentication.models.AuthenticationType import AuthenticationType


class AuthenticationChallengeAdapter:
    @staticmethod
    def to_challenge(authentication_method: AuthenticationType) -> str:
        mapping: dict[AuthenticationType, str] = {
            AuthenticationType.API_KEY: 'Api-Key realm="main", header="X-Api-Key"',
            AuthenticationType.BEARER_TOKEN: 'Bearer realm="main"',
            AuthenticationType.COOKIE_TOKEN: 'Bearer realm="main", token_location="cookie", cookie_name="access_token"',
        }
        return mapping.get(authentication_method, f'{authentication_method} realm="main"')
