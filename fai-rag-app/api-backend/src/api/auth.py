from fastapi import APIRouter
from pydantic import BaseModel

from src.modules.auth.auth_router_decorator import AuthRouterDecorator
from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth Test"]
)

auth = AuthRouterDecorator(auth_router)


class AuthTestResponseModel(BaseModel):
    message: str
    auth_identity: AuthenticatedIdentity


@auth.get(
    '/test',
    ['can_ask_questions'],
    summary='Test authentication/authorization endpoint',
    description='''
This endpoint does nothing except showcase how authenticated/authorized endpoints work. 

It also serves as a code example of how to implement an endpoint with auth (see source code).''',
    response_model=AuthTestResponseModel,
    response_description='Success. Returns the authentication details.'
)
async def auth_test(auth_identity: AuthenticatedIdentity):
    return AuthTestResponseModel(
        message='If you see this then everything works!',
        auth_identity=auth_identity)
