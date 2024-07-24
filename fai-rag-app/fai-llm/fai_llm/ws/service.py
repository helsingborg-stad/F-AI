from typing import Type

from fai_llm.assistant.models import AssistantTemplate, AssistantTemplateMeta, AssistantStreamConfig, \
    AssistantStreamMessage
from fai_llm.serializer.impl.json import JSONSerializer
from fai_llm.service_locator.service import global_locator
from fai_llm.worker.model import WorkStatus
from fai_llm.ws.model import WsMessages
from fai_llm.ws.protocol import IWebsocketClientConnection


class WebSocketClient:
    def __init__(self, conn: IWebsocketClientConnection, dc_exc_type: Type[Exception]):
        self._conn = conn
        self._dc_exc_type = dc_exc_type
        self._log = global_locator.services.main_logger.scope('WebSocketClient')
        self._serializer = JSONSerializer[WsMessages.Client]()
        self._my_job_ids = []
        self._payload_type_handlers = {
            'add': self._handle_add,
            'cancel': self._handle_cancel,
            'query': self._handle_query
        }

    async def _handle_add(self, payload: WsMessages.Client):
        self._log.debug(f'add, {payload.job_id} query={payload.query}')
        global_locator.services.worker_service.enqueue(
            job_id=payload.job_id,
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
            history=payload.history,
            query=payload.query
        )
        await self._add_job_handler(payload.job_id)

    async def _handle_cancel(self, payload: WsMessages.Client):
        self._log.debug(f'cancel, {payload.job_id}')

    async def _handle_query(self, payload: WsMessages.Client):
        self._log.debug(f'query, {payload.job_id}')
        await self._add_job_handler(payload.job_id)

    async def _add_job_handler(self, job_id: str):
        self._my_job_ids.append(job_id)
        await global_locator.services.worker_service.listen_for(job_id, self._on_job_update)

    async def _on_job_update(self, payload: WorkStatus):
        data = self._serializer.serialize(payload)
        await self._conn.send(data)

    async def run(self):
        self._log.info('connected')
        try:
            while True:
                msg = await self._conn.receive()
                self._log.info(f'received {msg}')
                payload = self._serializer.deserialize(msg, WsMessages.Client)
                await self._payload_type_handlers[payload.command](payload)

        except self._dc_exc_type:
            self._log.info('disconnected')

        finally:
            for job_id in self._my_job_ids:
                global_locator.services.worker_service.stop_listen_for(job_id)
