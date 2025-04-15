from src.modules.groups.protocols.IGroupService import IGroupService
from src.modules.resources.protocols.IResourceService import IResourceService


class GroupBasedResourceService(IResourceService):
    def __init__(self, group_service: IGroupService):
        self._group_service = group_service

    async def get_resources(self, as_uid: str) -> list[str]:
        groups = await self._group_service.get_groups_by_member(member=as_uid)
        all_resources = set(r for g in groups for r in g.resources)
        return list(all_resources)

    async def filter_accessible_resources(self, as_uid: str, resources: list[str]) -> list[str]:
        return [r for r in resources if r in await self.get_resources(as_uid=as_uid)]

    async def can_access(self, as_uid: str, resource: str) -> bool:
        return resource in await self.get_resources(as_uid=as_uid)
