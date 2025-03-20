import os

from src.modules.groups.protocols.IGroupService import IGroupService


async def setup_default_groups(group_service: IGroupService):
    await group_service.create_group(
        new_id='ff0000000000000000000000',
        owner=os.environ['SETUP_ADMIN'],
        label='default',
        members=['*@*'],
        scopes=[]
    )

    await group_service.create_group(
        new_id='ff0000000000000000000001',
        owner='',
        label='admins',
        members=[os.environ['SETUP_ADMIN']],
        scopes=[
            'apiKey.read',
            'apiKey.write',
            'assistant.read',
            'assistant.write',
            'collection.read',
            'collection.write',
            'conversation.read',
            'conversation.write',
            'document.chunk',
            'group.read',
            'group.write',
            'llm.run',
            'settings.read',
            'settings.write',
            'test'
        ]
    )
