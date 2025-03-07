from pydantic import BaseModel


class ConfirmedLogin(BaseModel):
    user_id: str
    access_token: str
