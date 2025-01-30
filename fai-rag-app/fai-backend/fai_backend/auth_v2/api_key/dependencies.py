from fai_backend.auth_v2.api_key.service import ApiKeyService
from fai_backend.repositories import api_key_repo


async def get_api_key_service() -> ApiKeyService:
    return ApiKeyService(repo=api_key_repo)
