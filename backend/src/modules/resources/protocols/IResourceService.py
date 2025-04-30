from typing import Protocol


class IResourceService(Protocol):
    async def get_resources(self, as_uid: str) -> list[str]:
        ...

    async def filter_accessible_resources(self, as_uid: str, resources: list[str]) -> list[str]:
        ...

    async def can_access(self, as_uid: str, resource: str) -> bool:
        ...

    async def set_resource_visibility(self, as_uid: str, resource: str, public: bool) -> bool:
        ...
