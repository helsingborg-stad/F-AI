import uuid

from fai_backend.auth_v2.api_key.models import ApiKeyDocumentModel, ApiKeyModel, ReadOnlyApiKeyModel
from fai_backend.repository.interface import IAsyncRepo


class ApiKeyService:
    def __init__(self, repo: IAsyncRepo[ApiKeyDocumentModel]):
        self._repo = repo

    async def create(self, scopes: list[str]) -> (str, str):
        key = f'fai-{uuid.uuid4().hex}'
        api_key = ApiKeyModel(key=key, scopes=scopes)
        new_entry = await self._repo.create(ApiKeyDocumentModel(api_key=api_key))
        return new_entry.id, key

    async def revoke(self, key_repo_id: str):
        await self._repo.delete(key_repo_id)

    async def list(self) -> list[ReadOnlyApiKeyModel]:
        all_keys = await self._repo.list()
        return [ApiKeyService._to_read_only_api_key(key_data) for key_data in all_keys]

    async def find_by_key(self, key: str) -> ReadOnlyApiKeyModel | None:
        all_keys = await self._repo.list()
        return next(
            (ApiKeyService._to_read_only_api_key(key_data) for key_data in all_keys if key_data.api_key.key == key),
            None)

    async def find_by_revoke_id(self, revoke_id: str) -> ReadOnlyApiKeyModel | None:
        all_keys = await self._repo.list()
        return next(
            (ApiKeyService._to_read_only_api_key(key_data) for key_data in all_keys if
             str(key_data.id) == revoke_id),
            None)

    @staticmethod
    def _to_read_only_api_key(key_data):
        return ReadOnlyApiKeyModel(
            revoke_id=str(key_data.id),
            redacted_key=ApiKeyService._redact_key(key_data.api_key.key),
            scopes=key_data.api_key.scopes,
        )

    @staticmethod
    def _redact_key(key: str) -> str:
        return key[:8] + "..." + key[-4:]
