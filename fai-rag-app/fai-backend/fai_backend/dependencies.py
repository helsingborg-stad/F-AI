from typing import Optional

from fastapi import Depends, HTTPException, Security

from fai_backend.auth.dependencies import (
    get_auth_service,
    try_get_access_token_payload,
)
from fai_backend.auth.schema import TokenPayload
from fai_backend.auth.service import AuthService
from fai_backend.schema import User


async def try_get_authenticated_user(
    payload: Optional[TokenPayload] = Security(try_get_access_token_payload),
    auth_service: AuthService = Depends(get_auth_service),
) -> Optional[User]:
    try:
        return await auth_service.users_repo.get_user_by_email(payload.email)
    except Exception as _:
        return None


async def get_authenticated_user(
    user: Optional[User] = Depends(try_get_authenticated_user),
) -> User:
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
