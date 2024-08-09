from starlette.websockets import WebSocket

from fai_llm.ws.protocol import IWebsocketClientConnection


class StarletteConnection(IWebsocketClientConnection):
    def __init__(self, connection: WebSocket):
        self._connection = connection

    async def send(self, data: str):
        await self._connection.send_text(data)

    async def receive(self) -> str:
        return await self._connection.receive_text()
