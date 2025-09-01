from typing import Protocol

from src.modules.models.models.Model import Model


class IModelService(Protocol):
    async def get_available_models(self, as_uid: str) -> list[Model]:
        ...

    async def set_available_models(self, models: list[Model]) -> bool:
        ...

    async def create_model(self, model: Model, as_uid: str) -> bool:
        ...

    async def get_model(self, key: str, as_uid: str) -> Model | None:
        ...

    async def update_model(self, key: str, model: Model, as_uid: str) -> bool:
        ...

    async def delete_model(self, key: str, as_uid: str) -> bool:
        ...