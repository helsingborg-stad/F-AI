import asyncio
import logging
import threading
from asyncio import Queue
from typing import List, AsyncGenerator

import sys
import websockets
from websockets import WebSocketClientProtocol

from fai_backend.assistant.models import WsMessages, GenerateRequest, ActiveRequest, MessagePart
from fai_backend.config import settings
from fai_backend.serializer.impl.json import JSONSerializer


class LLMWorkerConnection:
    _thread: threading.Thread
    _main_to_ws_thread_pending_requests: Queue[(GenerateRequest, ActiveRequest)] = Queue()
    _active_requests: List[ActiveRequest] = []

    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.setLevel(logging.DEBUG)
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(
            logging.Formatter('%(asctime)s:%(name)s:%(process)d:%(thread)d:%(levelname)s:%(message)s'))
        self._log.addHandler(stdout_handler)

        self._serializer = JSONSerializer[WsMessages.Base]()

        self._message_handlers = {
            'resp_add': self._on_msg_resp_add,
            'running': self._on_msg_running,
            'done': self._on_msg_done
        }

        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

        self._log.debug('worker started')

    async def ask_generator(self, request: GenerateRequest) -> AsyncGenerator[MessagePart, None]:
        active_request = ActiveRequest(local_id=request.id)
        self._active_requests.append(active_request)

        # Send request to websocket thread
        await self._main_to_ws_thread_pending_requests.put(request)

        # handle messages back from websocket thread
        while True:
            msg = await active_request.ws_to_main_thread_pending_updates.get()
            if msg.for_id == request.id:
                yield msg

                if msg.is_final:
                    break

    """
    Helpers
    """

    def _get_active_request_by_local_id(self, local_id: str) -> ActiveRequest:
        return next(r for r in self._active_requests if r.local_id == local_id)

    def _get_active_request_by_remote_id(self, remote_id: str) -> ActiveRequest:
        return next(r for r in self._active_requests if r.remote_id == remote_id)

    """
    Handlers for incoming messages (from remote LLM worker over websocket)
    """

    async def _on_msg_resp_add(self, data: WsMessages.AddResponse):
        # self._log.debug(f'_on_add, {data=}')
        ar = self._get_active_request_by_local_id(data.id)
        ar.remote_id = data.job_id

    async def _on_msg_running(self, data: WsMessages.JobUpdateResponse):
        ar = self._get_active_request_by_remote_id(data.job_id)
        await ar.ws_to_main_thread_pending_updates.put(
            MessagePart(for_id=ar.local_id, part=data.message))

    async def _on_msg_done(self, data: WsMessages.JobDoneResponse):
        ar = self._get_active_request_by_remote_id(data.job_id)
        await ar.ws_to_main_thread_pending_updates.put(
            MessagePart(for_id=ar.local_id, is_final=True))

    """
    Websocket thread things
    """

    async def _check_messages_from_main_thread(self, ws: WebSocketClientProtocol):
        while not self._main_to_ws_thread_pending_requests.empty():
            to_send = await self._main_to_ws_thread_pending_requests.get()
            ws_request = WsMessages.AddRequest(
                id=to_send.id,
                assistant=to_send.assistant,
                history=to_send.history,
                query=to_send.query
            )
            self._log.info(f'sending, {ws_request=}')
            await ws.send(self._serializer.serialize(ws_request))

    async def _check_messages_from_remote_server(self, ws: WebSocketClientProtocol):
        try:
            # use timeout to not block websocket thread main loop indefinitely
            async with asyncio.timeout(1):
                msg = await ws.recv()
            payload = self._serializer.deserialize(msg, WsMessages.Base)
            model_type = WsMessages.incoming_type_map[payload.type]
            validated = model_type.model_validate(payload.model_dump())
            await self._message_handlers[validated.type](validated)
        except TimeoutError:
            pass

    """
    Main websocket message loop that runs in a separate thread
    """

    def _run(self):
        async def body():
            while True:  # (re)try connection loop
                try:
                    self._log.info(f'connecting to {settings.LLM_WORKER_URI}...')
                    async with websockets.connect(settings.LLM_WORKER_URI) as ws:
                        self._log.info(f"connected")
                        try:
                            while True:  # msg loop
                                await self._check_messages_from_main_thread(ws)
                                await self._check_messages_from_remote_server(ws)
                        except websockets.exceptions.ConnectionClosed:
                            self._log.info(f"connection closed", exc_info=True)
                except Exception:
                    self._log.info(f"connection failed", exc_info=True)
                await asyncio.sleep(5)  # TODO: back-off this incrementally for each retry attempt?

        asyncio.run(body())
