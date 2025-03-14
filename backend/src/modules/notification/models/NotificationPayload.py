from pydantic import BaseModel


class NotificationPayload(BaseModel):
    subject: str
    body: str
