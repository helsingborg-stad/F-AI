from typing import Type, Callable, Any, Awaitable

from fai_llm.assistant.models import AssistantTemplate, AssistantTemplateMeta, AssistantStreamConfig, \
    AssistantStreamMessage
from fai_llm.serializer.impl.json import JSONSerializer
from fai_llm.service_locator.service import global_locator
from fai_llm.worker.model import WorkerMessages
from fai_llm.ws.model import WsMessages
from fai_llm.ws.protocol import IWebsocketClientConnection, IWebSocketClientHandler
from fai_llm.ws.worker_ws_adapter import WorkerToWsMessagesAdapter


class Handler(IWebSocketClientHandler):
    def __init__(self, sender_func: Callable[[Any], Awaitable[None]]):
        self._log = global_locator.services.main_logger.scope('WebSocketClientHandler')
        self._sender_func = sender_func

    async def add(self, payload: WsMessages.AddRequest):
        data = WsMessages.AddRequest.model_validate(payload)
        self._log.debug(f"add {payload}")
        new_job_id = global_locator.services.worker_service.enqueue(
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
        self._log.debug(f"add {data.id}={new_job_id}")
        await self._sender_func(WsMessages.AddResponse(
            id=data.id,
            job_id=new_job_id
        ))
        await self.listen(WsMessages.ListenRequest(job_id=new_job_id))

    async def listen(self, payload: WsMessages.ListenRequest):
        self._log.debug(f"listen {payload}")
        await global_locator.services.worker_service.listen_for(payload.job_id, self._send_job_update)

    async def _send_job_update(self, payload: WorkerMessages.Base):
        converted = WorkerToWsMessagesAdapter.to_ws(payload)
        await self._sender_func(converted)


class WebSocketClient:
    def __init__(self, conn: IWebsocketClientConnection, dc_exc_type: Type[Exception]):
        self._conn = conn
        self._dc_exc_type = dc_exc_type
        self._log = global_locator.services.main_logger.scope('WebSocketClient')
        self._serializer = JSONSerializer[WsMessages.Base]()
        self._handler = Handler(sender_func=self._send)

        self._my_job_ids = []
        self._payload_type_handlers = {
            'add': self._handler.add,
            'listen': self._handler.listen
        }

    async def _send(self, data: Any):
        serialized = self._serializer.serialize(data)
        await self._conn.send(serialized)

    async def run(self):
        self._log.info('connected')
        try:
            while True:
                msg = await self._conn.receive()
                self._log.info(f'received {msg}')
                payload = self._serializer.deserialize(msg, WsMessages.Base)
                model_type = WsMessages.incoming_type_map[payload.type]
                validated = model_type.model_validate(payload.model_dump())
                await self._payload_type_handlers[payload.type](validated)

        except self._dc_exc_type:
            self._log.info('disconnected')

        finally:
            for job_id in self._my_job_ids:
                global_locator.services.worker_service.stop_listen_for(job_id)
