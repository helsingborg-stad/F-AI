import asyncio

import pytest

from src.common.get_timestamp import get_timestamp
from src.modules.conversations.protocols.IConversationService import IConversationService


class BaseConversationServiceTestClass:
    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_conversation_service_create_get(service: IConversationService):
        conversation_id = await service.create_conversation('my_assistant_id')
        conversation = await service.get_conversation(conversation_id)

        assert conversation_id
        assert conversation
        assert conversation.id == conversation_id
        assert conversation.title == ''
        assert conversation.assistant_id == 'my_assistant_id'
        assert len(conversation.messages) == 0

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_conversation_service_get_none(service: IConversationService):
        result = await service.get_conversation('does not exist')
        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_conversation_service_list(service: IConversationService):
        await service.create_conversation('a')
        await service.create_conversation('b')

        conversations = await service.get_conversations()

        assert len(conversations) == 2
        assert next(c for c in conversations if c.assistant_id == 'a')
        assert next(c for c in conversations if c.assistant_id == 'b')

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_conversation_service_add_message(service: IConversationService):
        conversation_id = await service.create_conversation('my_assistant_id')
        timestamp = get_timestamp()

        success1 = await service.add_message_to_conversation(conversation_id, timestamp, 'system', 'Answer truthfully')
        success2 = await service.add_message_to_conversation(conversation_id, timestamp, 'user', 'What is 2+2')
        success3 = await service.add_message_to_conversation(conversation_id, timestamp, 'assistant', '4')

        conversation = await service.get_conversation(conversation_id)
        assert conversation
        assert success1 is True
        assert success2 is True
        assert success3 is True
        assert len(conversation.messages) == 3
        assert conversation.messages[0].timestamp == timestamp
        assert conversation.messages[0].role == 'system'
        assert conversation.messages[0].content == 'Answer truthfully'
        assert conversation.messages[1].role == 'user'
        assert conversation.messages[1].content == 'What is 2+2'
        assert conversation.messages[2].role == 'assistant'
        assert conversation.messages[2].content == '4'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_conversation_service_add_message_invalid(service: IConversationService):
        result = await service.add_message_to_conversation('does not exist', '', '', '')
        assert result is False

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_add_to_conversation_last_message(service: IConversationService):
        conversation_id = await service.create_conversation('my_assistant_id')
        timestamp = get_timestamp()

        success1 = await service.add_message_to_conversation(conversation_id, timestamp, 'system', 'Answer truthfully')
        success2 = await service.add_message_to_conversation(conversation_id, timestamp, 'user', 'What is 2+2')
        success3 = await service.add_message_to_conversation(conversation_id, timestamp, '', '')

        await asyncio.sleep(1)
        new_timestamp = get_timestamp()

        result1 = await service.add_to_conversation_last_message(conversation_id, new_timestamp, 'assistant', 'I')
        result2 = await service.add_to_conversation_last_message(conversation_id, new_timestamp, 'assistant',
                                                                 ' think it')
        result3 = await service.add_to_conversation_last_message(conversation_id, new_timestamp, 'assistant', '\'s 4.')

        conversation = await service.get_conversation(conversation_id)

        assert conversation
        assert success1 is True
        assert success2 is True
        assert success3 is True
        assert result1 is True
        assert result2 is True
        assert result3 is True
        assert len(conversation.messages) == 3
        assert conversation.messages[-1].timestamp == new_timestamp
        assert conversation.messages[-1].role == 'assistant'
        assert conversation.messages[-1].content == 'I think it\'s 4.'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_add_to_conversation_last_message_invalid(service: IConversationService):
        result = await service.add_to_conversation_last_message('does not exist', '', '', '')
        assert result is False

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_add_to_conversation_last_message_auto_creates(service: IConversationService):
        conversation_id = await service.create_conversation('my_assistant_id')

        timestamp = get_timestamp()
        result = await service.add_to_conversation_last_message(conversation_id, timestamp, 'system', 'hello world')

        conversation = await service.get_conversation(conversation_id)

        assert result is True
        assert len(conversation.messages) == 1
        assert conversation.messages[0].timestamp == timestamp
        assert conversation.messages[0].role == 'system'
        assert conversation.messages[0].content == 'hello world'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_conversation_service_set_title(service: IConversationService):
        conversation_id = await service.create_conversation('my_assistant_id')

        result = await service.set_conversation_title(conversation_id, 'my title')
        conversation = await service.get_conversation(conversation_id)

        assert result is True
        assert conversation.title == 'my title'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_conversation_service_set_title_invalid(service: IConversationService):
        result = await service.set_conversation_title('', '')
        assert result is False

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_conversation_service_delete(service: IConversationService):
        conversation_id = await service.create_conversation('my_assistant_id')
        await service.delete_conversation(conversation_id)
        conversation = await service.get_conversation(conversation_id)

        assert not conversation
