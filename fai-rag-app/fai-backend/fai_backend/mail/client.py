from abc import ABC, abstractmethod
from collections.abc import Callable

import requests
from pydantic import Field

from fai_backend.config import settings
from fai_backend.logger.console import console
from fai_backend.mail.schemas import EmailPayload
from fai_backend.settings.service import SettingsServiceFactory, SettingKey


class MailClient(ABC):
    @abstractmethod
    async def send_mail(self, payload: EmailPayload) -> bool:
        raise NotImplementedError


class ConsoleMailClient(MailClient):
    def __init__(self, send_handler: Callable[[EmailPayload], bool] = None):
        self.send_handler = send_handler if send_handler else lambda _payload: True

    async def send_mail(self, payload: EmailPayload) -> bool:
        console.log(payload)
        return self.send_handler(payload)


class BrevoPayload(EmailPayload):
    body: str = Field(..., serialization_alias='htmlContent')


class BrevoMailClient(MailClient):

    async def send_mail(self, payload: EmailPayload) -> bool:
        payload = BrevoPayload.model_validate(payload.model_dump())
        settings_service = SettingsServiceFactory().get_service()
        url = await settings_service.get_value(SettingKey.BREVO_API_URL)
        key = await settings_service.get_value(SettingKey.BREVO_API_KEY)
        headers = {
            'accept': 'application/json',
            'api-key': key,
            'content-type': 'application/json',
        }

        response = requests.post(
            url,
            json=payload.model_dump(by_alias=True, exclude_none=True),
            headers=headers,
        )

        return response.status_code == 201


async def create_mail_client() -> MailClient:
    settings_service = SettingsServiceFactory().get_service()
    key = await settings_service.get_value(SettingKey.BREVO_API_KEY)
    if len(key) > 0:
        print("using BrevoMailClient")
        return BrevoMailClient()
    print("using ConsoleMailClient")
    return ConsoleMailClient()
