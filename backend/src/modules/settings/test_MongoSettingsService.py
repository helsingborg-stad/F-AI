import pytest_asyncio
from pymongo.asynchronous.database import AsyncDatabase

from src.modules.settings.MongoSettingsService import MongoSettingsService
from src.modules.settings.test_settings_service import BaseSettingsServiceTest


@pytest_asyncio.fixture
def service(mongo_test_db: AsyncDatabase):
    return MongoSettingsService(mongo_test_db)


class TestMongoSettingsService(BaseSettingsServiceTest):
    ...
