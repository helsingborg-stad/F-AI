from pydantic import BaseModel


class AuthenticatedIdentity(BaseModel):
    uid: str
