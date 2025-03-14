from pydantic import BaseModel


class StoredOTP(BaseModel):
    user_id: str
    hashed_otp: str
