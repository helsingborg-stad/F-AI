import asyncio
import threading

import websockets
from websockets import WebSocketServerProtocol
from websockets.frames import CloseCode

from fai_llm.app_life.service import AppLifeService
from fai_llm.config.service import settings
from fai_llm.log.service import MPLogging
from fai_llm.service.ThreadedService import ThreadedService
from fai_llm.service_locator.service import global_locator


class WebSocketServerService(ThreadedService):
    def __init__(self):
        super().__init__()

    async def _run(self):
        async def _handle_connection(ws: WebSocketServerProtocol):
            self._log.debug(f'connection opened {ws.id}')

            try:
                while True:
                    msg = await ws.recv()
                    print(f'received: {type(msg)} {msg}')

                    if 'close' in msg:
                        break
                    else:
                        await ws.send(msg)

            except websockets.exceptions.ConnectionClosed:
                pass

            self._log.debug(f'connection closed {ws.id}')

        async with websockets.serve(_handle_connection, "localhost", 8765):
            self._log.info('started')
            while self._should_keep_running():
                await asyncio.sleep(1)


if __name__ == '__main__':
    settings.LOG_LEVEL = 'debug'
    settings.LOG_STDOUT = True
    global_locator.services.main_logger = MPLogging.get_logger('main')
    global_locator.services.app_life = AppLifeService()


    async def main():
        wss = WebSocketServerService()
        while True:
            await asyncio.sleep(1)


    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

    global_locator.services.app_life.shutdown()
