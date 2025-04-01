from src.modules.settings.models.SettingValue import SettingValue
from src.modules.settings.protocols.ISettingsService import ISettingsService


class MockSettingsService(ISettingsService):
    async def get_setting(self, key: str, fallback_value: SettingValue | None = None) -> SettingValue | None:
        return None

    async def get_settings(self) -> dict[str, SettingValue]:
        return {}

    async def set_setting(self, key: str, value: SettingValue) -> None:
        return None
