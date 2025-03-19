from src.modules.settings.models.SettingValue import SettingValue
from src.modules.settings.protocols.ISettingsService import ISettingsService


class MockSettingsService(ISettingsService):
    async def get_setting(self, key: str, fallback_value: SettingValue | None = None) -> SettingValue | None:
        return None

    async def get_str_setting(self, key: str, fallback_value: str | None = None) -> str | None:
        return None

    async def get_int_setting(self, key: str, fallback_value: int | None = None) -> int | None:
        return None

    async def get_float_setting(self, key: str, fallback_value: float | None = None) -> float | None:
        return None

    async def get_bool_setting(self, key: str, fallback_value: bool | None = None) -> bool | None:
        return None

    async def get_settings(self) -> dict[str, SettingValue]:
        return {}

    async def set_setting(self, key: str, value: SettingValue) -> None:
        return None
