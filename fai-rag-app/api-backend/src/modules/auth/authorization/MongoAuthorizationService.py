from pymongo.asynchronous.database import AsyncDatabase

from src.modules.api_key.protocols.IApiKeyService import IApiKeyService
from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity
from src.modules.auth.authorization.models.GrantedScopes import GrantedScopes
from src.modules.auth.authorization.protocols.IAuthorizationService import IAuthorizationService
from src.modules.auth.helpers.flatten_permissions import flatten_permissions, Permissions
from src.modules.groups.protocols.IGroupService import IGroupService


class MongoAuthorizationService(IAuthorizationService):
    def __init__(self, database: AsyncDatabase, api_key_service: IApiKeyService, group_service: IGroupService):
        self._database = database
        self._api_key_service = api_key_service
        self._group_service = group_service

    async def has_scopes(self, identity: AuthenticatedIdentity, scopes: list[str]) -> bool:
        identity_scopes = await self.get_scopes(identity)
        return all((scope in identity_scopes.global_scopes for scope in scopes))

    async def get_scopes(self, identity: AuthenticatedIdentity) -> GrantedScopes:
        # TODO: include resources

        match identity.principal_type:
            case 'application':
                api_key = await self._api_key_service.find_by_revoke_id(identity.uid)

                if api_key is not None:
                    return GrantedScopes(global_scopes=api_key.scopes)

            case 'user':
                groups = await self._group_service.get_groups_by_member(identity.uid)
                flattened = flatten_permissions([Permissions(
                    scopes=group.scopes,
                    resources=[]
                ) for group in groups])
                return GrantedScopes(global_scopes=flattened.scopes)

        return GrantedScopes(global_scopes=[])
