import os

from src.modules.groups.protocols.IGroupService import IGroupService


async def setup_default_groups(group_service: IGroupService):
    await group_service.create_group(
        force_id='ff0000000000000000000000',
        as_uid=os.environ['SETUP_ADMIN'],
        label='default',
        members=['*@*'],
        scopes=[
            'assistant.read',
            'conversation.read',
            'conversation.write',
            'chat',
            'model.read'
        ],
        resources=[]
    )

    await group_service.create_group(
        force_id='ff0000000000000000000001',
        as_uid=os.environ['SETUP_ADMIN'],
        label='admins',
        members=[os.environ['SETUP_ADMIN']],
        scopes=[
            'apiKey.read',
            'apiKey.write',
            'assistant.read',
            'assistant.write',
            'chat',
            'collection.read',
            'collection.write',
            'conversation.read',
            'conversation.write',
            'document.chunk',
            'group.read',
            'group.write',
            'ai.run',
            'model.read',
            'model.write',
            'settings.read',
            'settings.write',
            'test'
        ],
        resources=[]
    )
