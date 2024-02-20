from fastapi import Depends, HTTPException, Security

from fai_backend.auth.dependencies import (
    get_auth_service,
    try_get_access_token_payload,
)
from fai_backend.auth.schema import TokenPayload
from fai_backend.auth.service import AuthService
from fai_backend.schema import ProjectUser, User


async def try_get_authenticated_user(
        payload: TokenPayload | None = Security(try_get_access_token_payload),
        auth_service: AuthService = Depends(get_auth_service),
) -> User | None:
    try:
        return await auth_service.users_repo.get_user_by_email(payload.email)
    except Exception as _:
        return None


async def get_authenticated_user(
        user: User | None = Depends(try_get_authenticated_user),
) -> User:
    if not user:
        raise HTTPException(status_code=302, detail='Unauthorized', headers={'Location': '/api/login'})
    return user


async def try_get_project_user(
        user: User | None = Depends(try_get_authenticated_user),
) -> ProjectUser | None:
    return None if not user or len(user.projects) == 0 else ProjectUser(
        email=user.email,
        role=user.projects[0].role,
        project_id=user.projects[0].project_id,
        permissions=user.projects[0].permissions,
    )


async def get_project_user(
        user: ProjectUser | None = Depends(try_get_project_user),
) -> ProjectUser:
    if not user:
        raise HTTPException(status_code=302, detail='Unauthorized', headers={'Location': '/api/login'})

    return user
