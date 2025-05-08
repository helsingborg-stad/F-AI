import logging

import requests

from src.modules.notification.models.NotificationPayload import NotificationPayload
from src.modules.notification.protocols.INotificationService import INotificationService
from src.modules.settings.protocols.ISettingsService import ISettingsService
from src.modules.settings.settings import SettingKey


class BrevoEmailNotificationService(INotificationService):
    def __init__(self, settings_service: ISettingsService):
        self._settings_service = settings_service

    async def send_notification(self, recipient: str, payload: NotificationPayload):
        url = await self._settings_service.get_setting(SettingKey.BREVO_URL.key)
        key = await self._settings_service.get_setting(SettingKey.BREVO_API_KEY.key)

        response = requests.post(
            url,
            headers={
                'accept': 'application/json',
                'api-key': key,
                'content-type': 'application/json',
            },
            json={
                'sender': {
                    'name': await self._settings_service.get_setting(SettingKey.BREVO_SENDER_NAME.key),
                    'email': await self._settings_service.get_setting(SettingKey.BREVO_SENDER_EMAIL.key),
                },
                'to': [{'email': recipient}],
                'subject': payload.subject,
                'htmlContent': payload.body,
            }
        )

        if not response.ok:
            logging.error(f'Error sending notification: {response.status_code} {response.text}')
