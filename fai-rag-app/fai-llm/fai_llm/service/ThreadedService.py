import asyncio
import threading

from fai_llm.log.service import ScopeableLogger
from fai_llm.service_locator.service import global_locator


class ThreadedService:
    """
    Base class for a service that runs in a separate thread.

    Uses the global AppLifeService to gracefully handle shutdown.

    Also provides an internal scoped log instance named after the subclass.
    """

    _thread_shutdown_timeout = 5.0
    _thread_active = True
    _thread: threading.Thread
    _log: ScopeableLogger

    def __init__(self):
        self._log = global_locator.services.main_logger.scope(type(self).__name__)
        self._thread = threading.Thread(target=self.__internal_thread_entry_point)
        self._thread.start()
        global_locator.services.app_life.add_on_shutdown(self._on_shutdown)

    def __internal_thread_entry_point(self):
        asyncio.run(self._run())

    def _on_shutdown(self):
        self._thread_active = False
        self._thread.join(self._thread_shutdown_timeout)
        if self._thread.is_alive():
            self._log.error('failed to stop thread')
        else:
            self._log.info('stopped thread')

    def _should_keep_running(self):
        """
        Subclasses that are long-running thread (e.g. polling) should call this
        periodically to check if the thread should end and if so end it naturally.
        :return: True if the thread should keep running, False if thread should shut down.
        """
        return self._thread_active

    async def _run(self):
        """
        Thread body. Override to provide functionality.
        Use `self._should_keep_running()` to check if thread should end.
        """
