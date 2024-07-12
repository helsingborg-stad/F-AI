from tests.conversations.test_fixtures import *
from fai_backend.qaf.schema import QuestionFilterParams, GenerateAnswerPayload
from fai_backend.repository.query.component import LogicalExpression, AttributeAssignment


@pytest.mark.asyncio
async def test_create_conversation(
        setup_db,
        conversation_service,
        project_admin_user,
        create_dark_matter_question
):
    dark_matter_conversation = await conversation_service.create_conversation(
        project_admin_user.email,
        create_dark_matter_question
    )

    assert dark_matter_conversation is not None, "No conversation returned"
    assert dark_matter_conversation.messages[0].content == DARK_MATTER_QUESTION, "Incorrect question content"
    assert dark_matter_conversation.conversation_root_id is None, "Conversation root id should be None"
    assert dark_matter_conversation.conversation_active_id == dark_matter_conversation.conversation_id, \
        "Conversation root id and active id are not the same"


@pytest.mark.asyncio
async def test_filter_and_list_conversation(
        setup_db,
        conversation_service,
        project_admin_user,
        create_dark_matter_question
):
    await conversation_service.create_conversation(
        project_admin_user.email,
        create_dark_matter_question
    )

    query = LogicalExpression('AND', [
        AttributeAssignment('type', 'question'),
        AttributeAssignment('created_by', project_admin_user.email)
    ])

    empty_query_params = QuestionFilterParams()

    filter_result = await conversation_service.filter_and_list_conversation(
        query,
        query_params=empty_query_params
    )

    assert filter_result is not None, "No conversation returned"
    assert len(filter_result) == 1, "Incorrect number of conversations returned"
    assert filter_result[0].messages[0].content == DARK_MATTER_QUESTION, "Incorrect question content"


@pytest.mark.asyncio
async def test_create_inactive_copy_of_conversation(
        setup_db,
        conversation_service,
        project_admin_user,
        create_dark_matter_question
):
    dark_matter_conversation = await conversation_service.create_conversation(
        project_admin_user.email,
        create_dark_matter_question
    )

    dark_matter_conversation_copy = await conversation_service.create_inactive_copy_of_conversation(
        dark_matter_conversation.id
    )

    assert dark_matter_conversation_copy is not None, "No conversation suggestion returned"
    assert dark_matter_conversation_copy.id != dark_matter_conversation.id, \
        "ID should be unique and not copied from original"
    assert dark_matter_conversation_copy.conversation_id != dark_matter_conversation.conversation_id, \
        "Conversation ID should be unique and not copied from original conversation"
    assert dark_matter_conversation_copy.conversation_root_id == dark_matter_conversation.conversation_id, \
        "Root ID should point to original conversation"
    assert dark_matter_conversation_copy.messages[0].content == DARK_MATTER_QUESTION, "Incorrect question content"


@pytest.mark.asyncio
async def test_set_active_conversation(
        setup_db,
        conversation_service,
        project_admin_user,
        create_dark_matter_question
):
    dark_matter_conversation = await conversation_service.create_conversation(
        project_admin_user.email,
        create_dark_matter_question
    )

    dark_matter_copy = await conversation_service.create_inactive_copy_of_conversation(
        dark_matter_conversation.id
    )

    root_conversation_updated = await conversation_service.set_active_conversation(dark_matter_copy.id)

    assert root_conversation_updated.conversation_root_id is None, "Root ID should be None"
    assert root_conversation_updated.conversation_active_id == dark_matter_copy.conversation_id, \
        "Active ID should point to dark_matter_copy"

