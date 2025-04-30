from typing import Protocol


class ITokenService(Protocol):
    async def get_token_count(self, as_uid: str, assistant_id: str, message: str) -> int:
        ...

    async def get_token_count_with_history(self, as_uid: str, conversation_id: str, message: str) -> int:
        ...
