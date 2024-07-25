from typing import Protocol

from fai_llm.ws.model import WsMessages


class IWebsocketClientConnection(Protocol):
    async def send(self, data: str):
        ...

    async def receive(self) -> str:
        ...


class IWebSocketClientHandler(Protocol):
    async def add(self, payload: WsMessages.AddRequest):
        ...

    async def listen(self, payload: WsMessages.ListenRequest):
        ...
