from typing import Protocol

from src.modules.settings.models.SettingValue import SettingValue, SettingsDict


class ISettingsService(Protocol):
    async def get_setting(self, key: str, fallback_value: SettingValue | None = None) -> SettingValue | None:
        ...

    async def get_settings(self) -> SettingsDict:
        ...

    async def set_setting(self, key: str, value: SettingValue) -> None:
        ...

    async def patch_settings(self, patch: SettingsDict) -> None:
        ...
