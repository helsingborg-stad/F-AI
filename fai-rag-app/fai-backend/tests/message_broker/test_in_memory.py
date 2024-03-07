from asyncio import sleep

import pytest

from fai_backend.message_broker.memory import MemoryQueue
from fai_backend.message_broker.redis_queue import RedisQueue


def echo(value):
    return value


def test_memory_queue_enqueue_and_result():
    queue = MemoryQueue()

    test_value = "Hello, World!"
    job = queue.enqueue(echo, test_value)
    assert job is not None

    status = queue.get_status(job.id)
    assert status == "finished"

    result = queue.get_result(job.id)
    assert result == test_value
