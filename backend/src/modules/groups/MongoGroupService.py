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

    async def create_group(
            self,
            as_uid: str,
            label: str,
            members: list[str],
            scopes: list[str],
            resources: list[str],
            force_id: str | None = None
    ) -> str:
        if force_id and await self._database['groups'].find_one({'_id': ObjectId(force_id)}) is not None:
            return force_id
        result = await self._database['groups'].insert_one({
            '_id': ObjectId(force_id) if force_id else ObjectId(),
            'owner': as_uid,
            'label': label,
            'members': members,
            'scopes': scopes,
            'resources': resources,
        })

        return str(result.inserted_id)

    async def get_group_by_id(self, as_uid: str, group_id: str) -> Group | None:
        if not is_valid_mongo_id(group_id):
            return None
        doc = await self._database['groups'].find_one(
            {'_id': ObjectId(group_id)},
            projection=['_id', 'owner', 'label', 'members', 'scopes', 'resources']
        )
        group = self._doc_to_group(doc) if doc else None
        return group if group and group.owner == as_uid else None

    async def get_owned_groups(self, as_uid: str) -> list[Group]:
        cursor = self._database['groups'].find(
            {'owner': as_uid},
            projection=['_id', 'owner', 'label', 'members', 'scopes', 'resources']
        )
        return [self._doc_to_group(doc) async for doc in cursor]

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

    async def set_group_members(self, as_uid: str, group_id: str, members: list[str]) -> bool:
        if not is_valid_mongo_id(group_id):
            return False

        result = await self._database['groups'].update_one(
            {'_id': ObjectId(group_id), 'owner': as_uid},
            {'$set': {'members': members}}
        )

        return result.modified_count == 1

    async def set_group_scopes(self, as_uid: str, group_id: str, scopes: list[str]) -> bool:
        if not is_valid_mongo_id(group_id):
            return False

        result = await self._database['groups'].update_one(
            {'_id': ObjectId(group_id), 'owner': as_uid},
            {'$set': {'scopes': scopes}}
        )

        return result.modified_count == 1

    async def add_group_resource(self, as_uid: str, group_id: str, resource: str) -> bool:
        if not is_valid_mongo_id(group_id):
            return False

        result = await self._database['groups'].update_one(
            {'_id': ObjectId(group_id), 'owner': as_uid},
            {'$addToSet': {'resources': resource}}
        )

        return result.matched_count == 1

    async def remove_group_resource(self, as_uid: str, group_id: str, resource: str) -> bool:
        if not is_valid_mongo_id(group_id):
            return False

        result = await self._database['groups'].update_one(
            {'_id': ObjectId(group_id), 'owner': as_uid},
            {'$pull': {'resources': resource}}
        )

        return result.matched_count == 1

    async def delete_group(self, as_uid: str, group_id: str):
        if not is_valid_mongo_id(group_id):
            return

        await self._database['groups'].delete_one({'_id': ObjectId(group_id), 'owner': as_uid})

    @staticmethod
    def _doc_to_group(doc: Mapping[str, Any]) -> Group:
        return Group(
            id=str(doc['_id']),
            owner=doc['owner'],
            label=doc['label'],
            members=doc['members'],
            scopes=doc['scopes'],
            resources=doc['resources']
        )
