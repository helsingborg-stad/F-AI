import pytest_asyncio
from pymongo.asynchronous.database import AsyncDatabase

from src.modules.assistants.MongoAssistantService import MongoAssistantService
from src.modules.assistants.test_assistant_service import BaseAssistantServiceTestClass
from src.modules.groups.MongoGroupService import MongoGroupService
from src.modules.groups.protocols.IGroupService import IGroupService
from src.modules.resources.GroupBasedResourceService import GroupBasedResourceService


@pytest_asyncio.fixture
def group_service(mongo_test_db: AsyncDatabase):
    return MongoGroupService(mongo_test_db)


@pytest_asyncio.fixture
def service(mongo_test_db: AsyncDatabase, group_service: IGroupService):
    resource_service = GroupBasedResourceService(group_service)
    return MongoAssistantService(mongo_test_db, resource_service)


class TestMongoAssistantService(BaseAssistantServiceTestClass):
    ...
