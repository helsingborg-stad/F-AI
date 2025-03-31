import pytest_asyncio
from pymongo.asynchronous.database import AsyncDatabase

from src.modules.groups.MongoGroupService import MongoGroupService
from src.modules.groups.test_group_service import BaseGroupServiceTestClass


@pytest_asyncio.fixture
def service(mongo_test_db: AsyncDatabase):
    return MongoGroupService(mongo_test_db)


class TestMongoGroupServiceClass(BaseGroupServiceTestClass):
    ...
