import pytest
from pymongo.asynchronous.database import AsyncDatabase

from src.modules.conversations.MongoConversationService import MongoConversationService
from src.modules.conversations.test_conversation_service import do_test_conversation_service_create_get, \
    do_test_conversation_service_list, do_test_conversation_service_add_message, do_test_conversation_service_delete, \
    do_test_conversation_service_set_title, do_test_conversation_service_get_none, \
    do_test_conversation_service_add_message_missing, do_test_conversation_service_set_title_missing


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_MongoConversationService_create_get(mongo_test_db: AsyncDatabase):
    service = MongoConversationService(mongo_test_db)
    await do_test_conversation_service_create_get(service)


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_MongoConversationService_get_none(mongo_test_db: AsyncDatabase):
    service = MongoConversationService(mongo_test_db)
    await do_test_conversation_service_get_none(service)


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_MongoConversationService_list(mongo_test_db: AsyncDatabase):
    service = MongoConversationService(mongo_test_db)
    await do_test_conversation_service_list(service)


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_MongoConversationService_add_message(mongo_test_db: AsyncDatabase):
    service = MongoConversationService(mongo_test_db)
    await do_test_conversation_service_add_message(service)


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_MongoConversationService_add_message_missing(mongo_test_db: AsyncDatabase):
    service = MongoConversationService(mongo_test_db)
    await do_test_conversation_service_add_message_missing(service)


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_MongoConversationService_set_title(mongo_test_db: AsyncDatabase):
    service = MongoConversationService(mongo_test_db)
    await do_test_conversation_service_set_title(service)


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_MongoConversationService_set_title_missing(mongo_test_db: AsyncDatabase):
    service = MongoConversationService(mongo_test_db)
    await do_test_conversation_service_set_title_missing(service)


@pytest.mark.mongo
@pytest.mark.asyncio
async def test_MongoConversationService_delete(mongo_test_db: AsyncDatabase):
    service = MongoConversationService(mongo_test_db)
    await do_test_conversation_service_delete(service)
