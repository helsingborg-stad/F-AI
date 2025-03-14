import logging
import os

import requests

from src.modules.notification.models.NotificationPayload import NotificationPayload
from src.modules.notification.protocols.INotificationService import INotificationService


class BrevoEmailNotificationService(INotificationService):
    async def send(self, recipient: str, payload: NotificationPayload):
        url = os.environ['BREVO_URL']
        key = os.environ['BREVO_KEY']

        response = requests.post(
            url,
            headers={
                'accept': 'application/json',
                'api-key': key,
                'content-type': 'application/json',
            },
            json={
                'sender': {
                    'name': os.environ['BREVO_SENDER_NAME'],
                    'email': os.environ['BREVO_SENDER_EMAIL'],
                },
                'to': [{'email': recipient}],
                'subject': payload.subject,
                'htmlContent': payload.body,
            }
        )

        if not response.ok:
            logging.error(f'Error sending notification: {response.status_code} {response.text}')
