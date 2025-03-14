from typing import Literal

from pydantic import BaseModel


class AuthenticatedIdentity(BaseModel):
    uid: str
