from pydantic import BaseModel

from src.modules.auth.authentication.models.AuthenticationType import AuthenticationType


class AuthenticationSourceCredentials(BaseModel):
    auth_type: AuthenticationType
    credentials: str | None
