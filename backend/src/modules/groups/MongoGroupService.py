from typing import Mapping, Any

from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from src.common.mongo import is_valid_mongo_id
from src.modules.groups.helpers.is_wildcard_member_match import is_wildcard_member_match
from src.modules.groups.helpers.wildcard_member_pattern_regex import wildcard_member_pattern_regex
from src.modules.groups.models.Group import Group
from src.modules.groups.protocols.IGroupService import IGroupService


class MongoGroupService(IGroupService):
    def __init__(self, database: AsyncDatabase):
        self._database = database

    async def get_groups_by_member(self, member: str) -> list[Group]:
        cursor = self._database['groups'].find(
            {'members': {'$in': [member, wildcard_member_pattern_regex]}},
            projection=['_id', 'owner', 'label', 'members', 'scopes', 'resources'])
        groups = [self._doc_to_group(doc) async for doc in cursor]
        direct_groups = [group for group in groups if member in group.members]
        indirect_groups = [group for group in groups if group not in direct_groups]
        matching_indirect_groups = [
            group for group in indirect_groups
            if any([
                is_wildcard_member_match(member, pattern)
                for pattern in group.members
                if '*' in pattern
            ])
        ]

        return direct_groups + matching_indirect_groups

    async def get_group_by_id(self, group_id: str) -> Group | None:
        if not is_valid_mongo_id(group_id):
            return None
        doc = await self._database['groups'].find_one({'_id': ObjectId(group_id)})
        return self._doc_to_group(doc) if doc else None

    async def create_group(self, new_id: str, owner: str, label: str, members: list[str], scopes: list[str]):
        if await self._database['groups'].find_one({'_id': ObjectId(new_id)}):
            return
        await self._database['groups'].insert_one({
            '_id': ObjectId(new_id),
            'owner': owner,
            'label': label,
            'members': members,
            'scopes': scopes,
            'resources': [],
        })

    async def delete_group(self, group_id: str):
        if not is_valid_mongo_id(group_id):
            return

        await self._database['groups'].delete_one({'_id': ObjectId(group_id)})

    async def get_groups(self) -> list[Group]:
        cursor = self._database['groups'].find()
        return [Group(
            id=str(doc['_id']),
            owner=doc['owner'],
            label=doc['label'],
            members=doc['members'],
            scopes=doc['scopes']
        )async for doc in cursor]

    async def set_group_members(self, group_id: str, members: list[str]):
        if not is_valid_mongo_id(group_id):
            return

        await self._database['groups'].update_one({'_id': ObjectId(group_id)}, {'$set': {'members': members}})

    async def set_group_scopes(self, group_id: str, scopes: list[str]):
        if not is_valid_mongo_id(group_id):
            return

        await self._database['groups'].update_one({'_id': ObjectId(group_id)}, {'$set': {'scopes': scopes}})

    @staticmethod
    def _doc_to_group(doc: Mapping[str, Any]) -> Group:
        return Group(
            id=str(doc['_id']),
            owner=doc['owner'],
            label=doc['label'],
            members=doc['members'],
            scopes=doc['scopes']
        )
