from typing import Protocol

from src.modules.groups.models.Group import Group


class IGroupService(Protocol):
    async def create_group(
            self,
            as_uid: str,
            label: str,
            members: list[str],
            scopes: list[str],
            resources: list[str],
            force_id: str | None = None
    ) -> str:
        ...

    async def get_group_by_id(self, as_uid: str, group_id: str) -> Group | None:
        ...

    async def get_owned_groups(self, as_uid: str) -> list[Group]:
        ...

    async def get_groups_by_member(self, member: str) -> list[Group]:
        ...

    async def set_group_members(self, as_uid: str, group_id: str, members: list[str]):
        ...

    async def set_group_scopes(self, as_uid: str, group_id: str, scopes: list[str]):
        ...

    async def add_group_resource(self, as_uid: str, group_id: str, resource: str):
        ...

    async def remove_group_resource(self, as_uid: str, group_id: str, resource: str):
        ...

    async def delete_group(self, as_uid: str, group_id: str):
        ...
