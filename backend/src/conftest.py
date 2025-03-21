import asyncio

import pytest_asyncio
from pymongo import AsyncMongoClient

from src.common.get_timestamp import get_timestamp


@pytest_asyncio.fixture
async def mongo_test_db():
    client = AsyncMongoClient('localhost')
    db_name = f"__FAI_TEST_DB_{get_timestamp().replace('.', '_')}"
    yield client[db_name]
    await client.drop_database(db_name)
    await client.close()
    await asyncio.sleep(1)  # Wait for cleanup to finish
