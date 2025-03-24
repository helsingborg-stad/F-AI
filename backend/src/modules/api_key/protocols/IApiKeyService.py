from typing import Protocol

from src.modules.api_key.models.NewlyCreatedApiKey import NewlyCreatedApiKey
from src.modules.api_key.models.RedactedApiKey import RedactedApiKey


class IApiKeyService(Protocol):
    async def create_api_key(self) -> NewlyCreatedApiKey:
        ...

    async def get_api_keys(self) -> list[RedactedApiKey]:
        ...

    async def find_api_key(self, key: str) -> RedactedApiKey | None:
        ...

    async def find_api_key_by_revoke_id(self, revoke_id: str) -> RedactedApiKey | None:
        ...

    async def revoke_api_key(self, revoke_id: str):
        ...
