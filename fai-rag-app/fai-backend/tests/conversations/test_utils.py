from tests.conversations.test_fixtures import *
from fai_backend.conversations.utils import *


@pytest.mark.asyncio
async def test_get_active_conversations_when_no_conversation_created_by_user_then_expect_no_conversations(
        conversation_service,
        setup_db,
        project_admin_user,
        create_dark_matter_question,
):
    active_conversations = await get_root_conversations_created_by_user(
        conversation_repo,
        project_admin_user.email
    )

    assert active_conversations is not None
    assert len(active_conversations) == 0


@pytest.mark.asyncio
async def test_create_one_active_conversation_then_expect_one_active_conversation_created(
        conversation_service,
        setup_db,
        project_admin_user,
        create_dark_matter_question,
):
    await conversation_service.create_conversation(
        project_admin_user.email,
        create_dark_matter_question
    )

    active_conversations = await get_root_conversations_created_by_user(
        conversation_repo,
        project_admin_user.email
    )

    assert active_conversations is not None
    assert len(active_conversations) == 1
    assert active_conversations[0].created_by == project_admin_user.email
    assert active_conversations[0].messages[0].content == DARK_MATTER_QUESTION


@pytest.mark.asyncio
async def test_create_two_active_conversation_then_expect_two_active_conversation_created(
        conversation_service,
        setup_db,
        project_admin_user,
        create_dark_matter_question,
        create_meaning_of_life_question
):
    await conversation_service.create_conversation(
        project_admin_user.email,
        create_dark_matter_question
    )

    await conversation_service.create_conversation(
        project_admin_user.email,
        create_meaning_of_life_question
    )

    active_conversations = await get_root_conversations_created_by_user(
        conversation_repo,
        project_admin_user.email
    )

    assert active_conversations is not None
    assert len(active_conversations) == 2

    questions_in_conversations = [conversation.messages[0].content for conversation in active_conversations]
    assert DARK_MATTER_QUESTION, MEANING_OF_LIFE_QUESTION in questions_in_conversations

    assert active_conversations[0].conversation_root_id is None
    assert active_conversations[1].conversation_root_id is None
    assert active_conversations[0].conversation_id == active_conversations[0].conversation_active_id
    assert active_conversations[1].conversation_id == active_conversations[1].conversation_active_id


@pytest.mark.asyncio
async def test_get_first_message_in_conversation_with_no_messages_then_expect_empty_list(
        conversation_service,
        setup_db,
        project_admin_user,
        create_dark_matter_question
):

    conversation = CreateConversationRequest(
        type='question',
        messages=[],
    )

    conversation = await conversation_service.create_conversation(
        project_admin_user.email,
        conversation
    )

    first_message = get_first_message_in_conversation(conversation)

    assert first_message is not None
    assert first_message == []


@pytest.mark.asyncio
async def test_get_first_message_in_conversation(
        conversation_service,
        setup_db,
        project_admin_user,
        create_dark_matter_question
):
    conversation = await conversation_service.create_conversation(
        project_admin_user.email,
        create_dark_matter_question
    )

    first_message = get_first_message_in_conversation(conversation)

    assert first_message is not None
    assert len(first_message) == 1


@pytest.mark.asyncio
async def test_get_last_message_in_conversation(
        conversation_service,
        setup_db,
        project_admin_user,
        create_dark_matter_question
):
    conversation = await conversation_service.create_conversation(
        project_admin_user.email,
        create_dark_matter_question
    )

    last_message = get_last_message_in_conversation(conversation)

    assert last_message is not None
    assert last_message[0].content == DARK_MATTER_QUESTION


@pytest.mark.asyncio
async def test_get_all_messages_in_conversation(
        conversation_service,
        setup_db,
        project_admin_user,
        create_dark_matter_question,
        create_meaning_of_life_question
):
    conversation = await conversation_service.create_conversation(
        project_admin_user.email,
        create_dark_matter_question
    )

    all_messages = get_all_messages_in_conversation(conversation)

    assert all_messages is not None
    assert len(all_messages) == 1
    assert all_messages[0].content == DARK_MATTER_QUESTION
    assert all_messages[0].created_by == project_admin_user.email
    assert all_messages[0].type == 'question'
