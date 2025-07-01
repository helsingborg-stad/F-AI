from fastapi import APIRouter, Response, HTTPException, status, Request
from pydantic import BaseModel, Field

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.auth.auth_router_decorator import AuthRouterDecorator
from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity

login_router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

auth = AuthRouterDecorator(login_router)


class InitiateLoginRequest(BaseModel):
    user_id: str = Field(examples=["john.smith@example.com"])


class InitiateLoginResponse(BaseModel):
    request_id: str = Field(examples=["abcdef1234567890"])


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
    request_id: str = Field(examples=["abcdef1234567890"])
    confirmation_code: str = Field(examples=["1234"])


class ConfirmLoginResponse(BaseModel):
    user_id: str = Field(examples=["john.smith@example.com"])


@login_router.post(
    '/confirm',
    description='''
Confirm a login previously started with `POST /login/initiate`.

If successful a cookie is set with a JWT for the authenticated user as well as the refresh token.
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
        secure=True,
        expires=login.access_token_expires_at
    )

    response.set_cookie(
        key='refresh_token',
        value=login.refresh_token,
        httponly=True,
        secure=True,
        expires=login.refresh_token_expires_at
    )

    return ConfirmLoginResponse(
        user_id=login.user_id
    )


class RefreshLoginResponse(BaseModel):
    user_id: str = Field(examples=["john.smith@example.com"])


@login_router.post(
    '/refresh',
    description='''
Refresh the login by using the refresh token cookie.

If successful a new access token and refresh token are set and the old refresh token is invalidated.
    ''',
    response_model=RefreshLoginResponse
)
async def refresh_login(request: Request, response: Response, services: ServicesDependency):
    try:
        refresh_token = request.cookies.get('refresh_token')

        if not refresh_token:
            raise ValueError("No refresh token cookie found")

        login = await services.login_service.refresh_login(refresh_token=refresh_token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    response.set_cookie(
        key='access_token',
        value=login.access_token,
        httponly=True,
        secure=True,
        expires=login.access_token_expires_at
    )

    response.set_cookie(
        key='refresh_token',
        value=login.refresh_token,
        httponly=True,
        secure=True,
        expires=login.refresh_token_expires_at
    )

    return RefreshLoginResponse(
        user_id=login.user_id
    )


@auth.post('/logout', [])
async def logout(request: Request, response: Response, auth_identity: AuthenticatedIdentity,
                 services: ServicesDependency):
    refresh_token = request.cookies.get('refresh_token')
    if refresh_token:
        await services.login_service.revoke_refresh_token(as_uid=auth_identity.uid,
                                                          refresh_token=refresh_token)
    response.delete_cookie(key='access_token')
    response.delete_cookie(key='refresh_token')


@auth.post(
    '/revoke/{refresh_token}',
    [],
    description='''
Revoke a specific refresh token.
    ''',
    status_code=status.HTTP_204_NO_CONTENT
)
async def revoke_token(refresh_token: str, auth_identity: AuthenticatedIdentity, services: ServicesDependency):
    await services.login_service.revoke_refresh_token(as_uid=auth_identity.uid, refresh_token=refresh_token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# TODO: kolla flera användare samtidigt och revokea varandras tokens
