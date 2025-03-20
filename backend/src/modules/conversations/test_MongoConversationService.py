import asyncio

import pytest
import pytest_asyncio
from pymongo import AsyncMongoClient

from src.common.get_timestamp import get_timestamp
from src.modules.conversations.MongoConversationService import MongoConversationService
from src.modules.conversations.test_conversation_service import do_test_conversation_service_create_get, \
    do_test_conversation_service_list, do_test_conversation_service_add_message, do_test_conversation_service_delete, \
    do_test_conversation_service_set_title


@pytest_asyncio.fixture
async def service():
    client = AsyncMongoClient('localhost')
    db_name = f"__FAI_TEST_DB_{get_timestamp().replace('.', '_')}"
    yield MongoConversationService(client[db_name])
    await client.drop_database(db_name)
    await client.close()
    await asyncio.sleep(1)  # Wait for cleanup to finish


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_MongoConversationService_create_get(service: MongoConversationService):
    await do_test_conversation_service_create_get(service)


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_MongoConversationService_list(service: MongoConversationService):
    await do_test_conversation_service_list(service)


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_MongoConversationService_add_message(service: MongoConversationService):
    await do_test_conversation_service_add_message(service)


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_MongoConversationService_set_title(service: MongoConversationService):
    await do_test_conversation_service_set_title(service)


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_MongoConversationService_delete(service: MongoConversationService):
    await do_test_conversation_service_delete(service)
