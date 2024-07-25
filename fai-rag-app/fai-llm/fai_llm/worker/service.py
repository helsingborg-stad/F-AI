import asyncio
import logging
import threading
import uuid
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection

from fai_llm.assistant.models import AssistantTemplate, AssistantStreamMessage, AssistantTemplateMeta, \
    AssistantStreamConfig
from fai_llm.assistant.service import AssistantFactory
from fai_llm.log.service import MPLogging
from fai_llm.service_locator.service import global_locator
from fai_llm.worker.model import WorkerMessages
from fai_llm.worker.protocol import IWorkerService, WorkCallback


class AssistantWorkerProcess(Process):
    POLL_INTERVAL = 1.0

    _log: logging.Logger

    def __init__(self, parent_connection: Connection):
        super().__init__()
        self._parent_connection = parent_connection

    def run(self):
        self._log = MPLogging.get_logger('AssistantWorkerProcess')
        self._log.info(f'started')

        async def wrap():
            try:
                while True:
                    while self._parent_connection.poll():
                        request = WorkerMessages.AddRequest(**self._parent_connection.recv().dict())
                        self._parent_connection.send(WorkerMessages.JobUpdate(job_id=request.job_id, message=''))
                        self._log.info(f'starting job {request.job_id}')
                        self._log.debug(request)

                        try:
                            async for part in self._run_assistant(request.assistant, request.history, request.query):
                                if part.final:
                                    self._parent_connection.send(
                                        WorkerMessages.JobUpdate(job_id=request.job_id, message=part.data))
                            self._parent_connection.send(WorkerMessages.JobDone(job_id=request.job_id))
                            self._log.info(f'job {request.job_id} completed successfully')
                        except Exception as e:
                            self._log.error(f'job {request.job_id} failed', exc_info=True)
                            self._parent_connection.send(WorkerMessages.JobError(job_id=request.job_id, error=str(e)))

                    await asyncio.sleep(self.POLL_INTERVAL)
            except:
                self._log.critical(f'crashed', exc_info=True)
                raise

        try:
            asyncio.run(wrap())
        except KeyboardInterrupt:
            self._log.info(f'received keyboard interrupt')
            exit(0)

    @staticmethod
    async def _run_assistant(assistant: AssistantTemplate, history: list[AssistantStreamMessage], query: str):
        factory = AssistantFactory()
        assistant_instance = factory.create_assistant(assistant)
        stream = await assistant_instance.create_stream(history)
        async for part in stream(query):
            yield part


class MPWorkerService(IWorkerService):
    POLL_INTERVAL = 1.0
    SHUTDOWN_TIMEOUT = 5.0

    _conn: Connection
    _log: logging.Logger
    _worker_process: AssistantWorkerProcess
    _polling_thread: threading.Thread
    _should_poll: bool = True
    _callbacks: dict[str, WorkCallback] = {}

    def __init__(self):
        self._log = global_locator.services.main_logger.scope('MPWorkerService')

        self._conn, self.remote_conn = Pipe(duplex=True)
        self._worker_process = AssistantWorkerProcess(parent_connection=self.remote_conn)
        self._worker_process.start()

        self._polling_thread = threading.Thread(target=self._poll)
        self._polling_thread.start()

        global_locator.services.app_life.add_on_shutdown(self._on_shutdown)

    def _on_shutdown(self):
        self._should_poll = False
        self._polling_thread.join(timeout=self.SHUTDOWN_TIMEOUT)
        if self._polling_thread.is_alive():
            self._log.error(f'failed to stop polling thread')
        else:
            self._log.info(f'stopped polling thread')

        self._worker_process.join(timeout=self.SHUTDOWN_TIMEOUT)
        if self._worker_process.is_alive():
            self._log.error(f'failed to stop worker process - terminating forcefully')
            self._worker_process.terminate()
            self._worker_process.join(timeout=self.SHUTDOWN_TIMEOUT)
        else:
            self._log.info(f'stopped worker process')
        self._worker_process.close()

        self._log.info('shutdown complete')

    def enqueue(
            self,
            assistant: AssistantTemplate,
            history: list[AssistantStreamMessage],
            query: str
    ) -> str:
        job_id = str(uuid.uuid4())
        self._conn.send(WorkerMessages.AddRequest(
            job_id=job_id,
            assistant=assistant,
            history=history,
            query=query,
        ))
        return job_id

    def cancel(self, job_id: str):
        raise NotImplementedError('cancel not implemented yet')

    async def listen_for(self, job_id: str, callback: WorkCallback):
        self._callbacks[job_id] = callback

    def stop(self, job_id: str):
        self._callbacks.pop(job_id, None)

    def _poll(self):
        async def poll_internal():
            self._log.debug('up and polling')
            while self._should_poll:
                if not self._worker_process.is_alive():
                    self._should_poll = False

                while self._conn.poll():
                    data = self._conn.recv()
                    self._log.debug(f'data, {data}')

                    if data.job_id in self._callbacks:
                        try:
                            await self._callbacks[data.job_id](data)
                        except Exception as e:
                            # A callback that fails should be considered invalid and be removed
                            self._log.warning(f'callback {data.job_id} failed: {str(e)}')
                            self._callbacks.pop(data.job_id, None)

                if not self._worker_process.is_alive():
                    self._log.critical(f'worker process died unexpectedly')
                    return

                if self._should_poll:
                    await asyncio.sleep(self.POLL_INTERVAL)

        asyncio.run(poll_internal())
