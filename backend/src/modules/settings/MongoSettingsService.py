from typing import Any

from pymongo.asynchronous.database import AsyncDatabase

from src.modules.settings.models.SettingValue import SettingValue
from src.modules.settings.protocols.ISettingsService import ISettingsService


class MongoSettingsService(ISettingsService):
    def __init__(self, database: AsyncDatabase):
        self._database = database

    async def get_setting(self, key: str, fallback_value: SettingValue | None = None) -> SettingValue | None:
        result = await self._database['settings'].find_one({'key': key}, projection=['key', 'value'])
        if result is None:
            return fallback_value
        return self._to_valid_value(result['value'])

    async def get_settings(self) -> dict[str, SettingValue]:
        cursor = self._database['settings'].find(projection=['key', 'value'])
        out_dict: dict[str, SettingValue] = {}
        async for doc in cursor:
            out_dict[doc['key']] = self._to_valid_value(doc['value'])
        return out_dict

    async def set_setting(self, key: str, value: SettingValue) -> None:
        await self._database['settings'].update_one({'key': key}, {'$set': {"value": value}}, upsert=True)

    @staticmethod
    def _to_valid_value(value: Any) -> SettingValue:
        if isinstance(value, str) or isinstance(value, int) or isinstance(value, float) or isinstance(value, bool):
            return value
        return str(value)
