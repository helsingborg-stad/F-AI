from dataclasses import dataclass

from src.modules.settings.models.SettingValue import SettingValue


@dataclass(frozen=True)
class Setting:
    key: str
    default: SettingValue

    def __str__(self) -> str:
        return self.key
