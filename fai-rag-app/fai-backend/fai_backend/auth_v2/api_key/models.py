from beanie import Document
from pydantic import BaseModel


class ApiKeyModel(BaseModel):
    key_hash: str
    key_hint: str
    scopes: list[str]


class ReadOnlyApiKeyModel(BaseModel):
    revoke_id: str
    key_hint: str
    scopes: list[str]


class ApiKeyDocumentModel(Document):
    api_key: ApiKeyModel

    class Settings:
        name = 'api_key'
