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

    async def set_resource_visibility(self, as_uid: str, resource: str, public: bool) -> bool:
        groups = await self._group_service.get_owned_groups(as_uid=as_uid)
        public_group = next((g for g in groups if g.label == '__public__'), None)

        if not public_group:
            gid = await self._group_service.create_group(as_uid=as_uid, label='__public__', members=['*@*'],
                                                         scopes=[], resources=[])
            public_group = await self._group_service.get_group_by_id(as_uid=as_uid, group_id=gid)

        if public and resource not in public_group.resources:
            return await self._group_service.add_group_resource(as_uid=as_uid, group_id=public_group.id,
                                                                resource=resource)

        elif not public and resource in public_group.resources:
            return await self._group_service.remove_group_resource(as_uid=as_uid, group_id=public_group.id,
                                                                   resource=resource)

        return False
