from typing import Protocol

from src.modules.assistants.models.Assistant import Assistant


class IAssistantService(Protocol):
    async def create_assistant(self) -> str:
        ...

    async def get_assistant(self, assistant_id: str) -> Assistant | None:
        ...

    async def get_assistants(self) -> list[Assistant]:
        ...

    async def update_assistant(
            self,
            assistant_id: str,
            name: str | None = None,
            description: str | None = None,
            allow_files: bool | None = None,
            sample_questions: list[str] | None = None,
            model: str | None = None,
            llm_api_key: str | None = None,
            instructions: str | None = None,
            temperature: float | None = None,
            max_tokens: int | None = None,
            collection_id: str | None = None,
    ) -> bool:
        ...

    async def delete_assistant(self, assistant_id: str) -> None:
        ...
