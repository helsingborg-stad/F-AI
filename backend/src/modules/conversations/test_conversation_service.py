import asyncio

import pytest

from src.common.get_timestamp import get_timestamp
from src.modules.conversations.protocols.IConversationService import IConversationService


class BaseConversationServiceTestClass:
    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_create_get(service: IConversationService):
        conversation_id = await service.create_conversation(as_uid='john', assistant_id='my_assistant_id')
        conversation = await service.get_conversation(as_uid='john', conversation_id=conversation_id)

        assert conversation_id
        assert conversation
        assert conversation.id == conversation_id
        assert conversation.title == ''
        assert conversation.assistant_id == 'my_assistant_id'
        assert len(conversation.messages) == 0

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_invalid_uid(service: IConversationService):
        conversation_id = await service.create_conversation(as_uid='john', assistant_id='a')

        result = await service.get_conversation(as_uid='jane', conversation_id=conversation_id)

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_invalid_id(service: IConversationService):
        result = await service.get_conversation(as_uid='john', conversation_id='does not exist')
        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_title_defaults_to_user_message(service: IConversationService):
        cid = await service.create_conversation(as_uid='john', assistant_id='a')
        await service.add_message_to_conversation(
            as_uid='john',
            conversation_id=cid,
            timestamp=get_timestamp(),
            role='system',
            message='Answer truthfully'
        )
        await service.add_message_to_conversation(
            as_uid='john',
            conversation_id=cid,
            timestamp=get_timestamp(),
            role='user',
            message='Hello how are you?'
        )

        result1 = await service.get_conversation(as_uid='john', conversation_id=cid)
        result2 = await service.get_conversations(as_uid='john')

        assert result1.title == 'Hello how are you?'
        assert result2[0].title == 'Hello how are you?'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_conversations(service: IConversationService):
        await service.create_conversation(as_uid='john', assistant_id='a')
        await service.create_conversation(as_uid='john', assistant_id='b')
        await service.create_conversation(as_uid='jane', assistant_id='c')

        conversations = await service.get_conversations(as_uid='john')

        assert len(conversations) == 2
        # conversations should be returned order of latest first
        assert conversations[0].assistant_id == 'b'
        assert conversations[1].assistant_id == 'a'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_add_message(service: IConversationService):
        conversation_id = await service.create_conversation(as_uid='john', assistant_id='a')
        timestamp = get_timestamp()

        success1 = await service.add_message_to_conversation(
            as_uid='john',
            conversation_id=conversation_id,
            timestamp=timestamp, role='system',
            message='Answer truthfully'
        )
        success2 = await service.add_message_to_conversation(
            as_uid='john',
            conversation_id=conversation_id,
            timestamp=timestamp, role='user', message='What is 2+2'
        )
        success3 = await service.add_message_to_conversation(
            as_uid='john',
            conversation_id=conversation_id,
            timestamp=timestamp, role='assistant', message='4'
        )

        conversation = await service.get_conversation(as_uid='john', conversation_id=conversation_id)
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
    async def test_add_message_invalid_uid(service: IConversationService):
        cid = await service.create_conversation(as_uid='john', assistant_id='a')

        success = await service.add_message_to_conversation(
            as_uid='jane',
            conversation_id=cid,
            timestamp=get_timestamp(),
            role='user',
            message='hello'
        )
        result = await service.get_conversation(as_uid='john', conversation_id=cid)

        assert success is False
        assert len(result.messages) == 0

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_add_message_invalid_id(service: IConversationService):
        result = await service.add_message_to_conversation('john', 'does not exist', '', '', '')
        assert result is False

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_add_to_conversation_last_message(service: IConversationService):
        conversation_id = await service.create_conversation(as_uid='john', assistant_id='my_assistant_id')
        timestamp = get_timestamp()

        success1 = await service.add_message_to_conversation(
            as_uid='john',
            conversation_id=conversation_id,
            timestamp=timestamp,
            role='system',
            message='Answer truthfully'
        )
        success2 = await service.add_message_to_conversation(
            as_uid='john',
            conversation_id=conversation_id,
            timestamp=timestamp,
            role='user',
            message='What is 2+2'
        )
        success3 = await service.add_message_to_conversation(
            as_uid='john',
            conversation_id=conversation_id,
            timestamp=timestamp,
            role='',
            message=''
        )

        await asyncio.sleep(1)
        new_timestamp = get_timestamp()

        result1 = await service.add_to_conversation_last_message(
            as_uid='john',
            conversation_id=conversation_id,
            timestamp=new_timestamp,
            role='assistant',
            additional_message='I'
        )
        result2 = await service.add_to_conversation_last_message(
            as_uid='john',
            conversation_id=conversation_id,
            timestamp=new_timestamp,
            role='assistant',
            additional_message=' think it'
        )
        result3 = await service.add_to_conversation_last_message(
            as_uid='john',
            conversation_id=conversation_id,
            timestamp=new_timestamp,
            role='assistant',
            additional_message='\'s 4.'
        )

        conversation = await service.get_conversation(as_uid='john', conversation_id=conversation_id)

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
    async def test_add_to_conversation_last_message_invalid_uid(service: IConversationService):
        conversation_id = await service.create_conversation(as_uid='john', assistant_id='my_assistant_id')
        await service.add_message_to_conversation(as_uid='john', conversation_id=conversation_id,
                                                  timestamp=get_timestamp(), role='system', message='hello')

        success = await service.add_to_conversation_last_message(as_uid='jane', conversation_id=conversation_id,
                                                                 timestamp=get_timestamp(), role='system',
                                                                 additional_message='world')

        result = await service.get_conversation(as_uid='john', conversation_id=conversation_id)

        assert success is False
        assert result.messages[0].content == 'hello'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_add_to_conversation_last_message_invalid_id(service: IConversationService):
        result = await service.add_to_conversation_last_message(
            as_uid='john', conversation_id='does not exist', timestamp='', role='', additional_message='')
        assert result is False

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_add_to_conversation_last_message_auto_creates(service: IConversationService):
        conversation_id = await service.create_conversation(as_uid='john', assistant_id='my_assistant_id')

        timestamp = get_timestamp()
        result = await service.add_to_conversation_last_message('john', conversation_id, timestamp, 'system',
                                                                'hello world')

        conversation = await service.get_conversation(as_uid='john', conversation_id=conversation_id)

        assert result is True
        assert len(conversation.messages) == 1
        assert conversation.messages[0].timestamp == timestamp
        assert conversation.messages[0].role == 'system'
        assert conversation.messages[0].content == 'hello world'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_title(service: IConversationService):
        conversation_id = await service.create_conversation(as_uid='john', assistant_id='my_assistant_id')

        result = await service.set_conversation_title(as_uid='john', conversation_id=conversation_id, title='my title')
        conversation = await service.get_conversation(as_uid='john', conversation_id=conversation_id)

        assert result is True
        assert conversation.title == 'my title'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_title_invalid_uid(service: IConversationService):
        conversation_id = await service.create_conversation(as_uid='john', assistant_id='my_assistant_id')

        success = await service.set_conversation_title(as_uid='jane', conversation_id=conversation_id, title='my title')
        result = await service.get_conversation(as_uid='john', conversation_id=conversation_id)

        assert success is False
        assert result.title == ''

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_title_invalid_id(service: IConversationService):
        result = await service.set_conversation_title(as_uid='john', conversation_id='does not exist', title='my title')
        assert result is False

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete(service: IConversationService):
        cid = await service.create_conversation(as_uid='john', assistant_id='my_assistant_id')
        await service.delete_conversation(as_uid='john', conversation_id=cid)
        result = await service.get_conversation(as_uid='john', conversation_id=cid)

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete_invalid_uid(service: IConversationService):
        cid = await service.create_conversation(as_uid='john', assistant_id='my_assistant_id')
        await service.delete_conversation(as_uid='jane', conversation_id=cid)
        result = await service.get_conversation(as_uid='john', conversation_id=cid)

        assert result is not None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete_invalid_id(service: IConversationService):
        await service.delete_conversation(as_uid='john', conversation_id='does not exist')

        result = await service.get_conversation(as_uid='john', conversation_id='does not exist')

        assert result is None
