from src.modules.groups.protocols.IGroupService import IGroupService
from src.modules.resources.GroupBasedResourceService import GroupBasedResourceService
from src.modules.resources.protocols.IResourceService import IResourceService


class ResourceServiceFactory:
    def __init__(self, group_service: IGroupService):
        self.group_service = group_service

    def get(self) -> IResourceService:
        return GroupBasedResourceService(group_service=self.group_service)
