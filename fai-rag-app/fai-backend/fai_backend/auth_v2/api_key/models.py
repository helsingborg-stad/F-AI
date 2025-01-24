from beanie import Document
from pydantic import BaseModel


class ApiKeyModel(BaseModel):
    key: str
    scopes: list[str]


class ReadOnlyApiKeyModel(BaseModel):
    revoke_id: str
    redacted_key: str
    scopes: list[str]


class ApiKeyDocumentModel(Document):
    api_key: ApiKeyModel

    class Settings:
        name = 'api_key'
