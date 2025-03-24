import asyncio
import shutil
import uuid

import pytest
import pytest_asyncio
from pymongo import AsyncMongoClient

from src.common.get_timestamp import get_timestamp
from src.common.mock_services import MockSettingsService
from src.modules.vector.ChromaDBVectorService import ChromaDBVectorService

TEST_DB_PATH = './__test_chromadb'


@pytest.fixture
def vector_service():
    path = TEST_DB_PATH + uuid.uuid4().hex
    shutil.rmtree(path, ignore_errors=True)
    yield ChromaDBVectorService(settings_service=MockSettingsService(), db_path=path)
    shutil.rmtree(path, ignore_errors=True)


@pytest_asyncio.fixture
async def mongo_test_db():
    client = AsyncMongoClient('localhost')
    db_name = f"__FAI_TEST_DB_{get_timestamp().replace('.', '_')}"
    yield client[db_name]
    await client.drop_database(db_name)
    await client.close()
    await asyncio.sleep(1)  # Wait for cleanup to finish
