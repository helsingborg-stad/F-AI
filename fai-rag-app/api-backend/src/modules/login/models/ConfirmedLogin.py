from pydantic import BaseModel


class ConfirmedLogin(BaseModel):
    user_id: str
    scopes: list[str]
    access_token: str
    # refresh_token: str
