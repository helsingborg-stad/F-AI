from typing import Protocol

from src.modules.login.models.ConfirmedLogin import ConfirmedLogin


class ILoginService(Protocol):
    async def initiate(self, user_id: str) -> str:
        ...

    async def confirm(self, request_id: str, confirmation_code: str) -> ConfirmedLogin:
        ...
