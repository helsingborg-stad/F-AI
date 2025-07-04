from datetime import datetime

from pydantic import BaseModel


class ConfirmedLogin(BaseModel):
    user_id: str
    access_token: str
    access_token_expires_at: datetime
    refresh_token: str
    refresh_token_expires_at: datetime
