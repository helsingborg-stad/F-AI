from fastapi import APIRouter, Response, HTTPException, status
from pydantic import BaseModel, Field

from src.common.services.fastapi_get_services import ServicesDependency

login_router = APIRouter(
    prefix="/login",
    tags=["Login"]
)


class InitiateLoginRequest(BaseModel):
    user_id: str = Field(example="john.smith@example.com")


class InitiateLoginResponse(BaseModel):
    request_id: str = Field(example="abcdef1234567890")


@login_router.post(
    '/initiate',
    description='''
Initiate a login for the given user. A confirmation code
is sent to the user. The code together with the unique 
request ID returned by this endpoint is used to confirm 
the login process via the `POST /login/confirm` endpoint.
    ''',
    response_model=InitiateLoginResponse,
)
async def initiate_login(body: InitiateLoginRequest, services: ServicesDependency):
    request_id = await services.login_service.initiate_login(user_id=body.user_id)
    return InitiateLoginResponse(request_id=request_id)


class ConfirmLoginRequest(BaseModel):
    request_id: str = Field(example="abcdef1234567890")
    confirmation_code: str = Field(example="1234")


class ConfirmLoginResponse(BaseModel):
    user_id: str = Field(example="john.smith@example.com")


@login_router.post(
    '/confirm',
    description='''
Confirm a login previously started with `POST /login/initiate`.

If successful a cookie is set with a JWT for the authenticated user.
    ''',
    response_model=ConfirmLoginResponse
)
async def confirm_login(response: Response, body: ConfirmLoginRequest, services: ServicesDependency):
    try:
        login = await services.login_service.confirm_login(request_id=body.request_id,
                                                           confirmation_code=body.confirmation_code)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    response.set_cookie(
        key='access_token',
        value=login.access_token,
        httponly=True,
    )

    return ConfirmLoginResponse(
        user_id=login.user_id
    )


@login_router.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key='access_token')
