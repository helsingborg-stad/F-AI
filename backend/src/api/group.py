from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.auth.auth_router_decorator import AuthRouterDecorator
from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity

group_router = APIRouter(
    prefix='/group',
    tags=['Group']
)

auth = AuthRouterDecorator(group_router)


class CreateGroupRequest(BaseModel):
    label: str


class CreateGroupResponse(BaseModel):
    group_id: str


@auth.post(
    '',
    ['group.write'],
    summary='Create new group',
    description='',
    response_model=CreateGroupResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_group(
        body: CreateGroupRequest,
        auth_identity: AuthenticatedIdentity,
        services: ServicesDependency
):
    group_id = await services.group_service.create_group(
        as_uid=auth_identity.uid,
        label=body.label,
        members=[],
        scopes=[],
        resources=[]
    )

    return CreateGroupResponse(group_id=group_id)


class ListGroupsResponseGroup(BaseModel):
    id: str
    label: str
    members: list[str]
    scopes: list[str]
    resources: list[str]


class ListGroupsResponse(BaseModel):
    groups: list[ListGroupsResponseGroup]


@auth.get(
    '',
    ['group.read'],
    summary='List groups',
    description='',
    response_model=ListGroupsResponse
)
async def list_groups(auth_identity: AuthenticatedIdentity, services: ServicesDependency):
    groups = await services.group_service.get_owned_groups(as_uid=auth_identity.uid)
    return ListGroupsResponse(groups=[
        ListGroupsResponseGroup(
            id=group.id,
            label=group.label,
            members=group.members,
            scopes=group.scopes,
            resources=group.resources
        ) for group in groups
    ])


class GetGroupResponse(BaseModel):
    label: str
    members: list[str]
    scopes: list[str]
    resources: list[str]


@auth.get(
    '/{group_id}',
    ['group.read'],
    summary='Get group',
    description='',
    response_model=GetGroupResponse,
    response_404_description='Group not found'
)
async def get_group(group_id: str, auth_identity: AuthenticatedIdentity, services: ServicesDependency):
    group = await services.group_service.get_group_by_id(as_uid=auth_identity.uid, group_id=group_id)

    if group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return GetGroupResponse(
        label=group.label,
        members=group.members,
        scopes=group.scopes,
        resources=group.resources
    )


class SetGroupMembersRequest(BaseModel):
    members: list[str]


@auth.patch(
    '/{group_id}/members',
    ['group.write'],
    summary='Set group members',
    description='',
    response_404_description='Group not found'
)
async def set_group_members(group_id: str, body: SetGroupMembersRequest, auth_identity: AuthenticatedIdentity,
                            services: ServicesDependency):
    success = await services.group_service.set_group_members(as_uid=auth_identity.uid, group_id=group_id,
                                                             members=body.members)

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


class SetGroupScopesRequest(BaseModel):
    scopes: list[str]


@auth.patch(
    '/{group_id}/scopes',
    ['group.write'],
    summary='Set group scopes',
    description='',
    response_404_description='Group not found'
)
async def set_group_scopes(group_id: str, body: SetGroupScopesRequest, auth_identity: AuthenticatedIdentity,
                           services: ServicesDependency):
    if not await services.authorization_service.has_scopes(auth_identity, body.scopes):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Attempting to set scope(s) outside of caller's scopes")

    success = await services.group_service.set_group_scopes(as_uid=auth_identity.uid, group_id=group_id,
                                                            scopes=body.scopes)

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@auth.put(
    '/{group_id}/resources/{resource_id}',
    ['group.write'],
    summary='Add resource to group',
    response_404_description='Group not found'
)
async def add_group_resource(group_id: str, resource_id: str, auth_identity: AuthenticatedIdentity,
                             services: ServicesDependency):
    success = await services.group_service.add_group_resource(as_uid=auth_identity.uid, group_id=group_id,
                                                              resource=resource_id)

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@auth.delete(
    '/{group_id}/resources/{resource_id}',
    ['group.write'],
    summary='Delete resource from group',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_group_resource(group_id: str, resource_id: str, auth_identity: AuthenticatedIdentity,
                                services: ServicesDependency):
    await services.group_service.remove_group_resource(as_uid=auth_identity.uid, group_id=group_id,
                                                       resource=resource_id)


@auth.delete(
    '/{group_id}',
    ['group.write'],
    summary='Delete group',
    description='',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_group(group_id: str, auth_identity: AuthenticatedIdentity, services: ServicesDependency):
    await services.group_service.delete_group(as_uid=auth_identity.uid, group_id=group_id)
