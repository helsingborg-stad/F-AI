from typing import Protocol

from src.modules.api_key.models.NewlyCreatedApiKey import NewlyCreatedApiKey
from src.modules.api_key.models.RedactedApiKey import RedactedApiKey


class IApiKeyService(Protocol):
    async def create(self) -> NewlyCreatedApiKey:
        ...

    async def revoke(self, revoke_id: str):
        ...

    async def get_all(self) -> list[RedactedApiKey]:
        ...

    async def find_by_key(self, key: str) -> RedactedApiKey | None:
        ...

    async def find_by_revoke_id(self, revoke_id: str) -> RedactedApiKey | None:
        ...
