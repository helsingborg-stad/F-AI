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
            name: str,
            description: str,
            sample_questions: list[str],
            model: str,
            llm_api_key: str | None,
            instructions: str,
            temperature: float,
            max_tokens: int,
            allow_files: bool,
            collection_id: str,
    ) -> bool:
        ...

    async def delete_assistant(self, assistant_id: str) -> None:
        ...
