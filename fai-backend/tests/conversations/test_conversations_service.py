from typing import cast
from uuid import uuid4

import pytest
import pytest_asyncio
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from fai_backend.conversations.models import Conversation, Message
from fai_backend.conversations.service import ConversationService
from fai_backend.repositories import ConversationDocument, ConversationRepository
from fai_backend.repository.mongodb import MongoDBRepo
from fai_backend.schema import ProjectUser


def test_get_conversation_copy():
    project_user = ProjectUser(
        email='jane.doe@mail.com',
        role='user',
        project_id='1234',
        permissions={'can_ask_questions': True}
    )

    conversation = Conversation(
        id='temp_id',
        created_by=project_user.email,
        participants=[project_user.email],
        type='question',
        messages=[
            Message(
                user='user',
                created_by=project_user.email,
                content='Some question',
                type='question'
            )
        ]
    )

    conversation_copy = ConversationService.get_conversation_copy(conversation)

    assert conversation_copy.id != conversation.id
    assert conversation_copy.conversation_id != conversation.conversation_id
    assert conversation_copy.conversation_root_id == conversation.conversation_id
    assert conversation_copy.conversation_active_id is None


@pytest_asyncio.fixture
async def conversation_repo() -> ConversationRepository:
    await init_beanie(database=AsyncMongoMockClient().test_db, document_models=[ConversationDocument])
    yield MongoDBRepo[Conversation, ConversationDocument](Conversation, ConversationDocument)
    await ConversationDocument.get_motor_collection().drop()


@pytest.mark.asyncio
async def test_set_active_conversation(conversation_repo):
    conversation_service = ConversationService(conversation_repo)

    project_user = ProjectUser(
        email='jane.doe@mail.com',
        role='user',
        project_id='1234',
        permissions={'can_ask_questions': True}
    )

    root_conversation_id = uuid4()
    root_conversation = Conversation(
        id='temp_id',
        project_id='1234',
        created_by=project_user.email,
        participants=[project_user.email],
        type='question',
        messages=[
            Message(
                user='user',
                created_by=project_user.email,
                content='Some question',
                type='question'
            )
        ],
        conversation_id=root_conversation_id,
        conversation_root_id=None,
        conversation_active_id=root_conversation_id
    )

    root_conversation_in_db = await conversation_service.conversations_repo.create(root_conversation)

    conversation_copy = ConversationService.get_conversation_copy(root_conversation_in_db)
    conversation_copy_in_db = await conversation_service.conversations_repo.create(conversation_copy)

    updated_root_active_id = await conversation_service.set_active_conversation(conversation_copy_in_db)

    assert updated_root_active_id.conversation_active_id == conversation_copy_in_db.conversation_id
