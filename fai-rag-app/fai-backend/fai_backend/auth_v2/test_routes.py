from fastapi import APIRouter
from pydantic import BaseModel

from fai_backend.auth_v2.authentication.models import AuthenticatedIdentity
from fai_backend.auth_v2.fastapi_auth import AuthRouterDecorator

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth Test"]
)
auth = AuthRouterDecorator(router)


class AuthTestReturnModel(BaseModel):
    message: str
    auth_identity: AuthenticatedIdentity


@auth.get(
    '/test',
    ['can_ask_questions'],
    summary='Test authentication/authorization endpoint',
    description='''This endpoint does nothing except showcase how auth endpoints work. 
    
It also serves as a code example of how to implement an endpoint with auth (see source code).''',
    response_model=AuthTestReturnModel,
    response_description='Success. Returns the authentication details.'
)
async def auth_test(auth_identity: AuthenticatedIdentity):
    return AuthTestReturnModel(
        message='If you see this then everything works!',
        auth_identity=auth_identity)
