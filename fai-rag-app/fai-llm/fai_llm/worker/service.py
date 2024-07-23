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
from fai_llm.worker.model import WorkerMessages, OpaqueID, WorkStatus
from fai_llm.worker.protocol import IWorkerService


class AssistantWorkerProcess(Process):
    POLL_INTERVAL = 1.0

    _log: logging.Logger

    def __init__(self, parent_connection: Connection):
        super().__init__()
        self._parent_connection = parent_connection

    def run(self):
        self._log = MPLogging.get_logger('AssistantWorkerProcess')
        self._log.info(f'AssistantWorkerProcess started')

        async def wrap():
            try:
                while True:
                    while self._parent_connection.poll():
                        request = WorkerMessages.RunRequest(**self._parent_connection.recv().dict())
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
            except Exception as ex:
                self._log.critical(f'crashed', exc_info=True)
                self._parent_connection.send(WorkerMessages.ProcessCrash(error=f'{type(ex).__name__}: {ex}'))

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
    _history: dict[OpaqueID, WorkStatus] = {}
    _should_poll: bool = True

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

        print(f'mp worker service shutdown')

    def enqueue(self, assistant: AssistantTemplate, history: list[AssistantStreamMessage], query: str) -> OpaqueID:
        new_job_id = OpaqueID(uuid.uuid4())
        self._history[new_job_id] = WorkStatus(status='pending', message='')
        self._conn.send(WorkerMessages.RunRequest(
            job_id=new_job_id,
            assistant=assistant,
            history=history,
            query=query,
        ))
        return new_job_id

    def cancel(self, job_id: OpaqueID):
        raise NotImplementedError('cancel not implemented yet')

    def status(self, job_id: OpaqueID) -> WorkStatus:
        return self._history[job_id]

    def _poll(self):
        async def poll_internal():
            self._log.debug('up and polling')
            while self._should_poll:
                if not self._worker_process.is_alive():
                    self._should_poll = False

                while self._conn.poll():
                    data = self._conn.recv()

                    # handle message
                    if isinstance(data, WorkerMessages.JobUpdate):
                        update: WorkerMessages.JobUpdate = data
                        self._history[update.job_id].status = 'running'
                        self._history[update.job_id].message += update.message
                        self._log.debug(f'job {update.job_id} update, message={update.message}')

                    elif isinstance(data, WorkerMessages.JobDone):
                        update: WorkerMessages.JobDone = data
                        self._history[update.job_id].status = 'done'
                        self._log.debug(
                            f'job {update.job_id} done, message={self._history[update.job_id].message}')

                    elif isinstance(data, WorkerMessages.JobError):
                        error: WorkerMessages.JobError = data
                        self._history[error.job_id].status = 'failed'
                        self._history[error.job_id].message = error.error
                        self._log.error(f'job {error.job_id} error, message={error.error}')

                    elif isinstance(data, WorkerMessages.ProcessCrash):
                        error: WorkerMessages.ProcessCrash = data
                        self._log.critical(f'worker process crashed...{error.error}')

                    else:
                        self._log.warning(f'unhandled worker process message {type(data)=} {data=}')

                if not self._worker_process.is_alive():
                    self._log.critical(f'worker process died unexpectedly')
                    return

                if self._should_poll:
                    await asyncio.sleep(self.POLL_INTERVAL)

        asyncio.run(poll_internal())


if __name__ == '__main__':
    async def main():
        wps = MPWorkerService()
        wps.enqueue(
            assistant=AssistantTemplate(
                id='test',
                meta=AssistantTemplateMeta(),
                streams=[AssistantStreamConfig(
                    provider='openai',
                    settings={'model': 'gpt-3.5-turbo'},
                    messages=[
                        AssistantStreamMessage(
                            role='system',
                            content='You are an unhelpful assistant that answers questions in a sarcastic way.'
                        ),
                        AssistantStreamMessage(
                            role='user',
                            content='{query}'
                        )
                    ]
                )]
            ),
            history=[],
            query='Hello, how are you?'
        )


    asyncio.run(main())
