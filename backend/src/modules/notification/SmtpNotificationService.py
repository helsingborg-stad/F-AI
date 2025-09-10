import os
import smtplib

from src.modules.notification.models.NotificationPayload import NotificationPayload
from src.modules.notification.protocols.INotificationService import INotificationService
from src.modules.settings.protocols.ISettingsService import ISettingsService
from src.modules.settings.settings import SettingKey


class SmtpNotificationService(INotificationService):
    def __init__(self, settings_service: ISettingsService):
        self._settings_service = settings_service

    async def send_notification(self, recipient: str, payload: NotificationPayload):
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        host = os.environ['SMTP_HOST']
        port = int(os.environ['SMTP_PORT'])
        user = os.environ['SMTP_USER']
        password = os.environ['SMTP_PASSWORD']
        sender_name = await self._settings_service.get_setting(SettingKey.SMTP_SENDER_NAME.key)
        sender_email = await self._settings_service.get_setting(SettingKey.SMTP_SENDER_EMAIL.key)

        m = MIMEMultipart('alternative')
        m['Subject'] = payload.subject
        m['From'] = f'{sender_name} <{sender_email}>'
        m['To'] = recipient

        p1 = MIMEText(payload.body, 'plain')
        p2 = MIMEText(payload.body, 'html')
        m.attach(p1)
        m.attach(p2)

        with smtplib.SMTP(host, port) as smtp_server:
            smtp_server.set_debuglevel(1)
            smtp_server.login(user, str(password))
            smtp_server.sendmail(sender_email, recipient, m.as_string())
            print('mail sent')
