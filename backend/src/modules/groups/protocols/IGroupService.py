from typing import Protocol

from src.modules.groups.models.Group import Group


class IGroupService(Protocol):
    async def get_groups_by_member(self, member: str) -> list[Group]:
        ...

    async def get_group_by_id(self, group_id: str) -> Group | None:
        ...

    async def add(self, new_id: str, owner: str, label: str, members: list[str], scopes: list[str]):
        ...

    async def delete(self, group_id: str):
        ...

    async def list_all(self) -> list[Group]:
        ...

    async def set_members(self, group_id: str, members: list[str]):
        ...

    async def set_scopes(self, group_id: str, scopes: list[str]):
        ...
