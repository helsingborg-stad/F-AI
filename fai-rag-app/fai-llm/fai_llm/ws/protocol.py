from typing import Protocol


class IWebsocketClientConnection(Protocol):
    async def send(self, data: str):
        ...

    async def receive(self) -> str:
        ...
