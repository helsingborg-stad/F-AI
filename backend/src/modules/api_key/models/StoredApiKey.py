from pydantic import BaseModel


class StoredApiKey(BaseModel):
    key_hash: str
    key_hint: str
