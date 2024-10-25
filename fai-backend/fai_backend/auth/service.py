from fastapi import Response
from pydantic import EmailStr, SecretStr

from fai_backend.auth.schema import ResponseToken
from fai_backend.auth.security import (
    access_security,
    create_access_token,
    create_refresh_token,
    generate_pin_code,
    get_password_hash,
    refresh_security,
    verify_password,
)
from fai_backend.config import settings
from fai_backend.mail.client import MailClient
from fai_backend.mail.schemas import EmailPayload, EmailRecipient, EmailSender
from fai_backend.repositories import PinCodeModel, PinCodeRepository, UserRepository


class AuthService:
    users_repo: UserRepository
    user_pin_repo: PinCodeRepository
    mail_client: MailClient

    def __init__(self, users_repo: UserRepository, pins_repo: PinCodeRepository, mail_client: MailClient):
        self.pins_repo = pins_repo
        self.users_repo = users_repo
        self.mail_client = mail_client

    async def email_exists(self, email: EmailStr) -> bool:
        user = await self.users_repo.get_user_by_email(email)
        return user is not None

    async def session_exists(self, session_id: str) -> bool:
        session = await self.pins_repo.get(session_id)
        return session is not None

    async def create_pin(self, email: EmailStr) -> str:
        generated_pin = generate_pin_code()
        session = await self.pins_repo.create(
            PinCodeModel(
                email=email,
                hashed_pin=get_password_hash(generated_pin),
            )
        )

        self.mail_client.send_mail(
            EmailPayload(
                sender=EmailSender(
                    name=settings.MAIL_SENDER_NAME,
                    email=settings.MAIL_SENDER_EMAIL,
                ),
                to=[EmailRecipient(email=email)],
                subject='Your Login PIN',
                body=f'<html><head></head><body><p>Hello,</p><p>Login with this pin: {generated_pin}</p></body></html>',
            )
        )

        return session.model_dump()['id']

    async def validate_pin(self, session_id, pin: SecretStr):
        session = await self.pins_repo.get(session_id)
        if session and verify_password(pin.get_secret_value(), session.hashed_pin):
            # await self.pins_repo.delete(session_id)
            return True
        return False

    async def exchange_pin_for_token(
            self, session_id, pin: SecretStr, response: Response | None = None
    ) -> ResponseToken | None:
        session = (
            await self.pins_repo.get(session_id)
            if await self.session_exists(session_id)
            else None
        )

        if session and verify_password(pin.get_secret_value(), session.hashed_pin):
            email = session.email
            await self.pins_repo.delete(session_id)
            return await self.create_token(email, response)

        return None

    async def create_token(self, email, response: Response | None = None):
        subject = {'email': email}
        token = ResponseToken(
            access_token=create_access_token(subject),
            refresh_token=create_refresh_token(subject),
        )
        if token and response is not None:
            access_security.set_access_cookie(response, token.access_token)
            refresh_security.set_refresh_cookie(response, token.refresh_token)
        return token

    async def refresh_token(self, email, response: Response | None = None):
        return await self.create_token(email, response)
