from typing import Optional

from pydantic import BaseModel, EmailStr

from fai_backend.config import settings


class EmailSender(BaseModel):
    name: str = settings.MAIL_SENDER_NAME
    email: EmailStr = settings.MAIL_SENDER_EMAIL


class EmailRecipient(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class EmailPayload(BaseModel):
    sender: EmailSender = EmailSender()
    to: list[EmailRecipient]
    subject: str
    body: str
