from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, SecretStr


class TokenPayload(BaseModel):
    email: EmailStr


class RequestPin(BaseModel):
    email: EmailStr


class ResponsePin(BaseModel):
    email: EmailStr
    session_id: str = None


class RequestPinVerification(BaseModel):
    session_id: str
    pin: SecretStr


class ResponseToken(BaseModel):
    access_token: str
    refresh_token: str


class CustomHTTPAuthorizationCredentials(HTTPAuthorizationCredentials):
    is_disabled: bool
