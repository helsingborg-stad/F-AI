import pytest

from src.modules.api_key.protocols.IApiKeyService import IApiKeyService


class BaseApiKeyTestClass:
    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_create_api_key(service: IApiKeyService):
        result = await service.create_api_key()

        assert result
        assert len(result.api_key) > 0
        assert len(result.revoke_id) > 0

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_api_keys(service: IApiKeyService):
        key1 = await service.create_api_key()
        key2 = await service.create_api_key()

        result = await service.get_api_keys()

        assert len(result) == 2
        assert result[0].revoke_id == key1.revoke_id
        assert result[0].key_hint == key1.api_key[:8] + "..." + key1.api_key[-4:]
        assert result[1].revoke_id == key2.revoke_id
        assert result[1].key_hint == key2.api_key[:8] + "..." + key2.api_key[-4:]

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_find_api_key(service: IApiKeyService):
        key = await service.create_api_key()

        result = await service.find_api_key(key.api_key)

        assert result
        assert result.revoke_id == key.revoke_id

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_find_api_key_missing(service: IApiKeyService):
        result = await service.find_api_key('does not exist')
        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_find_api_key_by_revoke_id(service: IApiKeyService):
        key = await service.create_api_key()

        result = await service.find_api_key_by_revoke_id(key.revoke_id)

        assert result
        assert result.revoke_id == key.revoke_id

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_find_api_key_by_revoke_id_missing(service: IApiKeyService):
        result = await service.find_api_key_by_revoke_id('does not exist')
        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_revoke_api_key(service: IApiKeyService):
        key = await service.create_api_key()
        await service.revoke_api_key(key.revoke_id)
        result = await service.find_api_key(key.api_key)

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_revoke_api_key_missing(service: IApiKeyService):
        await service.revoke_api_key('does not exist')
        assert True
