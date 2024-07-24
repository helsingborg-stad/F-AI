import asyncio
import threading
from unittest.mock import Mock

from fai_llm.service.ThreadedService import ThreadedService
from fai_llm.service_locator.service import global_locator
from fai_llm.tests_common.test_setup_global_locator import setup_global_locator


class TestThreadedService(ThreadedService):

    def __init__(self, run_mock: Mock):
        self.run_mock = run_mock
        super().__init__()

    async def _run(self):
        self.run_mock(threading.get_ident())

        while self._should_keep_running():
            await asyncio.sleep(0.1)


def test_threaded_service():
    setup_global_locator()

    run_mock = Mock()

    service = TestThreadedService(run_mock=run_mock)
    self_thread_id = threading.get_ident()

    global_locator.services.app_life.shutdown()

    assert service.run_mock.call_count == 1
    assert service.run_mock.call_args[0][0] != self_thread_id
