import pytest

from src.common.get_timestamp import get_timestamp
from src.modules.conversations.models.Message import Message
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
            message=Message(
                timestamp=get_timestamp(),
                role='system',
                content='Answer truthfully'
            )
        )
        await service.add_message_to_conversation(
            as_uid='john',
            conversation_id=cid,
            message=Message(
                timestamp=get_timestamp(),
                role='user',
                content='Hello how are you?'
            )
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
            message=Message(
                timestamp=timestamp,
                role='system',
                content='Answer truthfully'
            )
        )
        success2 = await service.add_message_to_conversation(
            as_uid='john',
            conversation_id=conversation_id,
            message=Message(timestamp=timestamp, role='user', content='What is 2+2')
        )
        success3 = await service.add_message_to_conversation(
            as_uid='john',
            conversation_id=conversation_id,
            message=Message(timestamp=timestamp, role='assistant', content='4')
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
    async def test_add_message_full(service: IConversationService):
        conversation_id = await service.create_conversation(as_uid='john', assistant_id='a')
        timestamp = get_timestamp()
        success1 = await service.add_message_to_conversation(
            as_uid='john',
            conversation_id=conversation_id,
            message=Message(
                timestamp=timestamp,
                role='system',
                content='some content',
                reasoning_content='my reasoning content',
                tool_call_id='my_tool_call',
                tool_calls=[{
                    'id': 'cool_tool_id',
                    'type': 'function',
                    'function': {
                        'name': 'cool_func',
                        'arguments': '{"arg1": "val1", "arg2": "val2"}'
                    }
                }],
                context_message_override='some context message'
            )
        )

        conversation = await service.get_conversation(as_uid='john', conversation_id=conversation_id)
        message = conversation.messages[0]

        assert success1 is True
        assert message.timestamp == timestamp
        assert message.role == 'system'
        assert message.content == 'some content'
        assert message.reasoning_content == 'my reasoning content'
        assert message.tool_call_id == 'my_tool_call'
        assert message.tool_calls[0]['id'] == 'cool_tool_id'
        assert message.tool_calls[0]['type'] == 'function'
        assert message.tool_calls[0]['function']['name'] == 'cool_func'
        assert message.tool_calls[0]['function']['arguments'] == '{"arg1": "val1", "arg2": "val2"}'
        assert message.context_message_override == 'some context message'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_add_message_invalid_uid(service: IConversationService):
        cid = await service.create_conversation(as_uid='john', assistant_id='a')

        success = await service.add_message_to_conversation(
            as_uid='jane',
            conversation_id=cid,
            message=Message(timestamp=get_timestamp(), role='user', content='hello')
        )
        result = await service.get_conversation(as_uid='john', conversation_id=cid)

        assert success is False
        assert len(result.messages) == 0

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_add_message_invalid_id(service: IConversationService):
        result = await service.add_message_to_conversation(
            'john',
            'does not exist',
            message=Message(timestamp='', role='', content='')
        )
        assert result is False

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_add_message_continue_from_index(service: IConversationService):
        cid = await service.create_conversation(as_uid='john', assistant_id='a')
        timestamp = get_timestamp()
        await service.add_message_to_conversation('john', cid,
                                                  message=Message(timestamp='', role='system', content='A'))
        await service.add_message_to_conversation('john', cid, message=Message(timestamp='', role='user', content='B'))
        await service.add_message_to_conversation('john', cid,
                                                  message=Message(timestamp='', role='assistant', content='C'))
        await service.add_message_to_conversation('john', cid, message=Message(timestamp='', role='user', content='D'))
        await service.add_message_to_conversation('john', cid,
                                                  message=Message(timestamp='', role='assistant', content='E'))

        success = await service.add_message_to_conversation(
            'john',
            cid,
            message=Message(timestamp=timestamp, role='user', content='X'),
            continue_from_index=2
        )

        conversation = await service.get_conversation('john', cid)

        assert success is True
        assert len(conversation.messages) == 4
        assert conversation.messages[0].content == 'A'
        assert conversation.messages[1].content == 'B'
        assert conversation.messages[2].content == 'C'
        assert conversation.messages[3].timestamp == timestamp
        assert conversation.messages[3].role == 'user'
        assert conversation.messages[3].content == 'X'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_add_message_continue_from_index_invalid(service: IConversationService):
        cid = await service.create_conversation(as_uid='john', assistant_id='a')
        await service.add_message_to_conversation('john', cid,
                                                  message=Message(timestamp='', role='system', content='A'))

        success = await service.add_message_to_conversation(
            'john',
            cid,
            message=Message(timestamp='', role='user', content='B'),
            continue_from_index=1
        )

        conversation = await service.get_conversation('john', cid)

        assert success is False
        assert len(conversation.messages) == 1
        assert conversation.messages[0].content == 'A'
        assert conversation.messages[0].timestamp == ''
        assert conversation.messages[0].role == 'system'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_replace_last_conversation_message(service: IConversationService):
        cid = await service.create_conversation(as_uid='john', assistant_id='a')

        await service.add_message_to_conversation(
            as_uid='john',
            conversation_id=cid,
            message=Message(timestamp=get_timestamp(), role='system', content='Answer truthfully')
        )
        await service.add_message_to_conversation(
            as_uid='john',
            conversation_id=cid,
            message=Message(timestamp=get_timestamp(), role='user', content='What is 2+2')
        )
        await service.add_message_to_conversation(
            as_uid='john',
            conversation_id=cid,
            message=Message(timestamp=get_timestamp(), role='assistant', content='')
        )

        timestamp = get_timestamp()

        success = await service.replace_conversation_last_message(
            as_uid='john',
            conversation_id=cid,
            message=Message(timestamp=timestamp, role='assistant', content='the answer is 4')
        )

        conversation = await service.get_conversation(as_uid='john', conversation_id=cid)
        message = conversation.messages[-1]

        assert success is True
        assert message.timestamp == timestamp
        assert message.role == 'assistant'
        assert message.content == 'the answer is 4'
        assert len(conversation.messages) == 3

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_replace_last_conversation_message_invalid_uid(service: IConversationService):
        cid = await service.create_conversation(as_uid='john', assistant_id='a')
        await service.add_message_to_conversation(as_uid='john', conversation_id=cid,
                                                  message=Message(timestamp=get_timestamp(), role='system',
                                                                  content='hello'))

        success = await service.replace_conversation_last_message(as_uid='jane', conversation_id=cid,
                                                                  message=Message(timestamp=get_timestamp(),
                                                                                  role='user', content='world'))
        result = await service.get_conversation(as_uid='john', conversation_id=cid)

        assert success is False
        assert result.messages[0].content == 'hello'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_replace_last_conversation_message_invalid_cid(service: IConversationService):
        result = await service.replace_conversation_last_message(as_uid='john', conversation_id='does not exist',
                                                                 message=Message(timestamp=get_timestamp(), role='user',
                                                                                 content='world'))
        assert result is False

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
