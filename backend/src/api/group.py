from bson import ObjectId
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


@auth.post(
    '',
    ['group.write'],
    summary='Create new group',
    description=''
)
async def create_group(
        body: CreateGroupRequest,
        auth_identity: AuthenticatedIdentity,
        services: ServicesDependency
):
    await services.group_service.create_group(
        new_id=str(ObjectId()),
        owner=auth_identity.uid,
        label=body.label,
        members=[],
        scopes=[]
    )


class DeleteGroupRequest(BaseModel):
    group_id: str


@auth.delete(
    '',
    ['group.write'],
    summary='Delete group',
    description=''
)
async def delete_group(body: DeleteGroupRequest, services: ServicesDependency):
    await services.group_service.delete_group(group_id=body.group_id)


class ListGroupsResponseGroup(BaseModel):
    id: str
    label: str
    members: list[str]
    scopes: list[str]


class ListGroupsResponse(BaseModel):
    groups: list[ListGroupsResponseGroup]


@auth.get(
    '',
    ['group.read'],
    summary='List groups',
    description='',
    response_model=ListGroupsResponse
)
async def list_groups(services: ServicesDependency):
    groups = await services.group_service.get_groups()
    return ListGroupsResponse(groups=[
        ListGroupsResponseGroup(
            id=group.id,
            label=group.label,
            members=group.members,
            scopes=group.scopes
        ) for group in groups
    ])


class GetGroupResponse(BaseModel):
    label: str
    members: list[str]
    scopes: list[str]


@auth.get(
    '{group_id}',
    ['group.read'],
    summary='Get group',
    description='',
    response_model=GetGroupResponse
)
async def get_group(group_id: str, services: ServicesDependency):
    group = await services.group_service.get_group_by_id(group_id=group_id)

    if group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Group not found')

    return GetGroupResponse(label=group.label, members=group.members, scopes=group.scopes)


class SetGroupMembersRequest(BaseModel):
    members: list[str]


@auth.patch(
    '{group_id}/members',
    ['group.write'],
    summary='Set group members',
    description=''
)
async def set_group_members(group_id: str, body: SetGroupMembersRequest, services: ServicesDependency):
    await services.group_service.set_group_members(group_id=group_id, members=body.members)


class SetGroupScopesRequest(BaseModel):
    scopes: list[str]


@auth.patch(
    '{group_id}/scopes',
    ['group.write'],
    summary='Set group scopes',
    description=''
)
async def set_group_scopes(group_id: str, body: SetGroupScopesRequest, services: ServicesDependency,
                           auth_identity: AuthenticatedIdentity):
    if not await services.authorization_service.has_scopes(auth_identity, body.scopes):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Attempting to set scope(s) outside of caller's scopes")

    await services.group_service.set_group_scopes(group_id=group_id, scopes=body.scopes)
