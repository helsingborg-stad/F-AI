from typing import Any

from src.modules.settings.protocols.ISettingsService import ISettingsService
from src.modules.settings.settings import SettingKey


async def _set_if_not_set(
        existing: dict[str, Any],
        settings_service: ISettingsService,
        key: str,
        value: float | int | bool | str
):
    if key not in existing:
        await settings_service.set_setting(key, value)


async def setup_default_settings(settings_service: ISettingsService):
    all_settings = await settings_service.get_settings()

    for _, setting in SettingKey:
        await _set_if_not_set(all_settings, settings_service, setting.key, setting.default)
