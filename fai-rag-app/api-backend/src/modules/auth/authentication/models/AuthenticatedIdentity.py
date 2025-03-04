from typing import Literal

from pydantic import BaseModel


class AuthenticatedIdentity(BaseModel):
    principal_type: Literal['application', 'user']
    uid: str
