from abc import ABC, abstractmethod
from collections.abc import Callable

import requests
from pydantic import Field

from fai_backend.config import settings
from fai_backend.logger.console import console
from fai_backend.mail.schemas import EmailPayload


class MailClient(ABC):
    @abstractmethod
    def send_mail(self, payload: EmailPayload) -> bool:
        raise NotImplementedError


def create_mail_client() -> MailClient:
    class ConsoleMailClient(MailClient):
        def __init__(self, send_handler: Callable[[EmailPayload], bool] = None):
            self.send_handler = send_handler if send_handler else lambda _payload: True

        def send_mail(self, payload: EmailPayload) -> bool:
            console.log(payload)
            return self.send_handler(payload)

    class BrevoPayload(EmailPayload):
        body: str = Field(..., serialization_alias='htmlContent')

    class BrevoMailClient(MailClient):
        def send_mail(self, payload: EmailPayload) -> bool:
            payload = BrevoPayload.model_validate(payload.model_dump())
            url = settings.BREVO_API_URL
            headers = {
                'accept': 'application/json',
                'api-key': settings.BREVO_API_KEY,
                'content-type': 'application/json',
            }

            response = requests.post(
                url,
                json=payload.model_dump(by_alias=True, exclude_none=True),
                headers=headers,
            )

            return response.status_code == 201

    return {
        'console': ConsoleMailClient,
        'brevo': BrevoMailClient,
    }[settings.MAIL_CLIENT]()
