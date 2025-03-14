from typing import Protocol

from src.modules.settings.models.SettingValue import SettingValue


class ISettingsService(Protocol):
    async def get_setting(self, key: str, fallback_value: SettingValue) -> SettingValue | None:
        ...

    async def get_str_setting(self, key: str, fallback_value: str | None = None) -> str | None:
        ...

    async def get_int_setting(self, key: str, fallback_value: int | None = None) -> int | None:
        ...

    async def get_float_setting(self, key: str, fallback_value: float | None = None) -> float | None:
        ...

    async def get_bool_setting(self, key: str, fallback_value: bool | None = None) -> bool | None:
        ...

    async def get_all(self) -> dict[str, SettingValue]:
        ...

    async def set_setting(self, key: str, value: SettingValue) -> None:
        ...
