import pytest
import pytest_asyncio
from pymongo.asynchronous.database import AsyncDatabase

from src.modules.assistants.MongoAssistantService import MongoAssistantService
from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.conversations.MongoConversationService import MongoConversationService
from src.modules.conversations.protocols.IConversationService import IConversationService
from src.modules.groups.MongoGroupService import MongoGroupService
from src.modules.groups.protocols.IGroupService import IGroupService
from src.modules.resources.GroupBasedResourceService import GroupBasedResourceService
from src.modules.resources.protocols.IResourceService import IResourceService
from src.modules.token.helpers.get_conversation_assistant_model import get_conversation_assistant_model


@pytest_asyncio.fixture
def group_service(mongo_test_db: AsyncDatabase):
    yield MongoGroupService(mongo_test_db)


@pytest_asyncio.fixture
def resource_service(group_service: IGroupService):
    return GroupBasedResourceService(group_service)


@pytest_asyncio.fixture
def assistant_service(mongo_test_db: AsyncDatabase, resource_service: IResourceService):
    return MongoAssistantService(database=mongo_test_db, resource_service=resource_service)


@pytest_asyncio.fixture
def conversation_service(mongo_test_db: AsyncDatabase):
    return MongoConversationService(mongo_test_db)


class TestGetConversationAssistantModel:
    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_correct_value(assistant_service: IAssistantService, conversation_service: IConversationService):
        aid = await assistant_service.create_assistant(as_uid='john')
        await assistant_service.update_assistant(as_uid='john', assistant_id=aid, model='openai:some-gpt-model')
        cid = await conversation_service.create_conversation(as_uid='john', assistant_id=aid)

        result = await get_conversation_assistant_model(
            as_uid='john',
            assistant_service=assistant_service,
            conversation_service=conversation_service,
            conversation_id=cid
        )

        assert result is not None

        conversation, assistant, model_name = result

        assert conversation.id == cid
        assert assistant.id == aid
        assert model_name == 'some-gpt-model'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_invalid_conversation(assistant_service: IAssistantService,
                                        conversation_service: IConversationService):
        result = await get_conversation_assistant_model(
            as_uid='john',
            assistant_service=assistant_service,
            conversation_service=conversation_service,
            conversation_id='does not exist'
        )

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_invalid_assistant(assistant_service: IAssistantService,
                                     conversation_service: IConversationService):
        aid = await assistant_service.create_assistant(as_uid='john')
        await assistant_service.update_assistant(as_uid='john', assistant_id=aid, model='openai:some-gpt-model')
        cid = await conversation_service.create_conversation(as_uid='john', assistant_id=aid)
        await assistant_service.delete_assistant(as_uid='john', assistant_id=aid)

        result = await get_conversation_assistant_model(
            as_uid='john',
            assistant_service=assistant_service,
            conversation_service=conversation_service,
            conversation_id=cid
        )

        assert result is None
