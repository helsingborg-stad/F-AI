from pydantic import BaseModel


class RedactedApiKey(BaseModel):
    revoke_id: str
    key_hint: str
