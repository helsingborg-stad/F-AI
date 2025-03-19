from typing import Any

from src.modules.settings.protocols.ISettingsService import ISettingsService


async def _set_if_not_set(existing: dict[str, Any], settings_service: ISettingsService, key: str, value: str):
    if key not in existing:
        await settings_service.set_setting(key, value)


async def setup_default_settings(settings_service: ISettingsService):
    all_settings = await settings_service.get_settings()

    await _set_if_not_set(all_settings, settings_service, 'login.fixed_otp', '1234')
    await _set_if_not_set(all_settings, settings_service, 'jwt.user_secret', 'CHANGE THIS')
    await _set_if_not_set(all_settings, settings_service, 'brevo.url', 'https://api.brevo.com/v3/smtp/email')
