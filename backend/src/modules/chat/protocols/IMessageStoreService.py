from typing import Protocol


class IMessageStoreService(Protocol):
    async def store_message(self, message: str) -> str:
        ...

    async def consume_message(self, stored_message_id: str) -> str | None:
        ...
