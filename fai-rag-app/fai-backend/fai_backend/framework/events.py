from typing import Annotated, Literal

from pydantic import BaseModel, Field

__all__ = (
    'AuthEvent',
    'GoToEvent',
    # then `AnyEvent` itself
    'AnyEvent',
)


class AuthEvent(BaseModel):
    type: Literal['AuthEvent'] = 'AuthEvent'
    token: str | None = None
    url: str


class GoToEvent(BaseModel):
    type: Literal['GoToEvent'] = 'GoToEvent'
    url: str
    query: dict | None = None


AnyEvent = Annotated[
    AuthEvent | GoToEvent,
    Field(discriminator='type')
]
