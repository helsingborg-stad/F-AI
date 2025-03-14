from pydantic import BaseModel


class NewlyCreatedApiKey(BaseModel):
    revoke_id: str
    api_key: str
