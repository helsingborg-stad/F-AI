from typing import Protocol

from src.modules.assistants.models.Assistant import Assistant
from src.modules.assistants.models.Model import Model


class IAssistantService(Protocol):
    async def create_assistant(self, as_uid: str) -> str:
        ...

    async def get_available_models(self, as_uid: str) -> list[Model]:
        ...

    async def set_available_models(self, models: list[Model]) -> bool:
        ...

    async def get_assistant(self, as_uid: str, assistant_id: str, redact_key: bool = True) -> Assistant | None:
        ...

    async def get_owned_assistants(self, as_uid: str) -> list[Assistant]:
        ...

    async def get_available_assistants(self, as_uid: str) -> list[Assistant]:
        ...

    async def update_assistant(
            self,
            as_uid: str,
            assistant_id: str,
            name: str | None = None,
            description: str | None = None,
            allow_files: bool | None = None,
            sample_questions: list[str] | None = None,
            is_public: bool | None = None,
            model: str | None = None,
            llm_api_key: str | None = None,
            instructions: str | None = None,
            collection_id: str | None = None,
            extra_llm_params: dict[str, float | int | bool | str] | None = None
    ) -> bool:
        ...

    async def delete_assistant(self, as_uid: str, assistant_id: str) -> None:
        ...
