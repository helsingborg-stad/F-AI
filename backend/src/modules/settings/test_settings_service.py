import pytest

from src.modules.settings.protocols.ISettingsService import ISettingsService


class BaseSettingsServiceTest:
    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_setting(service: ISettingsService):
        await service.set_setting('test_key', 'test_value')

        result = await service.get_setting('test_key')

        assert result == 'test_value'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_setting_missing(service: ISettingsService):
        result = await service.get_setting('does not exist')

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_setting_fallback(service: ISettingsService):
        result = await service.get_setting('does not exist', 'hello')

        assert result == 'hello'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_str_setting(service: ISettingsService):
        await service.set_setting('test_str', 'test_value')

        result = await service.get_setting('test_str')

        assert result == 'test_value'
        assert type(result) is str

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_int_setting(service: ISettingsService):
        await service.set_setting('test_int', 123)

        result = await service.get_setting('test_int')

        assert result == 123
        assert type(result) is int

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_float_setting(service: ISettingsService):
        await service.set_setting('test_float', 456.789)

        result = await service.get_setting('test_float')

        assert result == 456.789
        assert type(result) is float

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_bool_setting(service: ISettingsService):
        await service.set_setting('test_bool', True)

        result = await service.get_setting('test_bool')

        assert result is True
        assert type(result) is bool

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_settings(service: ISettingsService):
        await service.set_setting('test_str', 'blablabla')
        await service.set_setting('test_int', 100000)
        await service.set_setting('test_float', 3.14159265358979)
        await service.set_setting('test_bool', False)

        result = await service.get_settings()

        assert result['test_str'] == 'blablabla'
        assert result['test_int'] == 100000
        assert result['test_float'] == 3.14159265358979
        assert result['test_bool'] is False
