import asyncio

import pytest

from src.modules.chat.protocols.IMessageStoreService import IMessageStoreService


class BaseMessageStoreServiceTestClass:
    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_message_store_service(service: IMessageStoreService):
        stored_message_id = await service.store_message('my stored question!')
        stored_message = await service.consume_message(stored_message_id=stored_message_id)
        stored_message_2 = await service.consume_message(stored_message_id=stored_message_id)
        stored_message_3 = await service.consume_message(stored_message_id='does not exist')

        assert len(stored_message_id) > 0
        assert stored_message == 'my stored question!'
        assert stored_message_2 is None
        assert stored_message_3 is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_message_store_service_expire(service: IMessageStoreService):
        stored_message_id = await service.store_message('my stored question!')

        await asyncio.sleep(2)

        result = await service.consume_message(stored_message_id=stored_message_id)

        assert result is None
