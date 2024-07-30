from tests.conversations.test_fixtures import *
from fai_backend.conversations.utils import get_all_messages_in_conversation
from fai_backend.qaf.schema import GenerateAnswerPayload, QuestionFilterParams, ApproveAnswerPayload
from fai_backend.qaf.service import QAFService


@pytest_asyncio.fixture
async def qaf_service():
    return QAFService()


@pytest.mark.asyncio
async def test_submit_new_question_then_expect_new_conversation_returned(
        qaf_service,
        conversation_service,
        project_admin_user
):
    question = "What is the meaning of life?"
    question_meta = {
        "errand_id": "sk-123",
        "subject": "Life"
    }
    question_tag = ["philosophy"]

    submit_question_result = await qaf_service.submit_new_question(
        conversation_service,
        project_admin_user,
        question,
        question_meta,
        question_tag
    )

    assert submit_question_result is not None, "No question returned"
    assert submit_question_result.type == "question", "Incorrect question type"
    assert submit_question_result.question.content == question, "Incorrect question in question content"
    assert submit_question_result.errand_id == question_meta["errand_id"], "Incorrect errand_id in question errand_id"
    assert submit_question_result.subject == question_meta["subject"], "Incorrect subject in question subject"
    assert submit_question_result.tags == question_tag, "Incorrect tags in question tags"


@pytest.mark.asyncio
async def test_add_answer_to_question_then_expect_answer_added(
        qaf_service,
        conversation_service,
        project_admin_user
):
    question = "What is the answer to life, the universe, and everything?"
    question_meta = {
        "errand_id": "sk-123",
        "subject": "Life"
    }
    question_tag = ["philosophy"]

    submit_question_result = await qaf_service.submit_new_question(
        conversation_service,
        project_admin_user,
        question,
        question_meta,
        question_tag
    )

    payload = GenerateAnswerPayload(
        question_id=submit_question_result.id,
        answer="42",
    )

    add_message_result = await qaf_service.add_message(
        project_admin_user,
        payload,
        conversation_service
    )

    assert add_message_result is not None, "No question returned"
    assert add_message_result.messages[1].content == payload.answer, "Incorrect answer in question messages"


@pytest.mark.asyncio
async def test_list_submitted_questions_when_no_questions_exist_then_expect_empty_list_returned(
        qaf_service,
        conversation_service,
        project_admin_user
):
    empty_filter_params = QuestionFilterParams()

    questions = await qaf_service.list_submitted_questions(project_admin_user, empty_filter_params,
                                                           conversation_service)

    assert len(questions) == 0, "Questions list is not empty"


@pytest.mark.asyncio
async def test_list_submitted_questions_when_questions_exist_then_expect_questions_returned(
        qaf_service,
        conversation_service,
        project_admin_user
):
    question = "How does gravity work?"
    question_meta = {
        "errand_id": "sk-123",
        "subject": "Physics"
    }
    question_tag = ["science"]

    await qaf_service.submit_new_question(
        conversation_service,
        project_admin_user,
        question,
        question_meta,
        question_tag
    )

    empty_filter_params = QuestionFilterParams()

    questions = await qaf_service.list_submitted_questions(project_admin_user, empty_filter_params,
                                                           conversation_service)

    assert len(questions) == 1, "Questions list is empty"
    assert questions[0].question.content == question, "Incorrect question in question content"
    assert questions[0].errand_id == question_meta["errand_id"], "Incorrect errand_id in question errand_id"
    assert questions[0].subject == question_meta["subject"], "Incorrect subject in question subject"
    assert questions[0].tags == question_tag, "Incorrect tags in question tags"


@pytest.mark.asyncio
async def test_get_submitted_question_details_then_expect_question_returned(
        qaf_service,
        conversation_service,
        project_admin_user
):
    question = "What is the speed of light?"
    question_meta = {
        "errand_id": "sk-123",
        "subject": "Physics"
    }
    question_tag = ["science"]

    submit_question_result = await qaf_service.submit_new_question(
        conversation_service,
        project_admin_user,
        question,
        question_meta,
        question_tag
    )

    question_details = await qaf_service.submitted_question_details(
        project_admin_user,
        submit_question_result.id,
        conversation_service
    )

    assert question_details is not None, "No question returned"
    assert question_details.question.content == question, "Incorrect question in question content"
    assert question_details.errand_id == question_meta["errand_id"], "Incorrect errand_id in question errand_id"
    assert question_details.subject == question_meta["subject"], "Incorrect subject in question subject"
    assert question_details.tags == question_tag, "Incorrect tags in question tags"


@pytest.mark.asyncio
async def test_submit_new_question_then_expect_active_thread_created_containing_question(
        qaf_service,
        project_admin_user,
        conversation_service
):
    question = "What is the meaning of life?"
    question_meta = {
        "errand_id": "sk-123",
        "subject": "Life"
    }
    question_tag = ["philosophy"]

    submit_result = await qaf_service.submit_new_question(
        conversation_service,
        project_admin_user,
        question,
        question_meta,
        question_tag
    )

    submitted_conversation = await conversation_service.get_conversation_by_id(submit_result.id)
    active_thread = get_all_messages_in_conversation(submitted_conversation)

    assert len(active_thread) == 1, "Incorrect number of messages in active thread"
    assert active_thread[0].content == question, "Incorrect question in active thread"
    assert active_thread[0].type == "question", "Incorrect type in active thread"
    assert active_thread[0].created_by == project_admin_user.email, "Incorrect created_by in active thread"


@pytest.mark.asyncio
async def test_add_feedback_to_answer_then_expect_feedback_added(
        qaf_service,
        conversation_service,
        project_admin_user
):
    question = "What is the answer to life, the universe, and everything?"
    question_meta = {
        "errand_id": "sk-123",
        "subject": "Life"
    }
    question_tag = ["philosophy"]

    submit_question_result = await qaf_service.submit_new_question(
        conversation_service,
        project_admin_user,
        question,
        question_meta,
        question_tag
    )

    answer = "42"
    answer_payload = GenerateAnswerPayload(
        question_id=submit_question_result.id,
        answer=answer,
    )

    await qaf_service.add_message(
        project_admin_user,
        answer_payload,
        conversation_service
    )

    payload = ApproveAnswerPayload(
        question_id=submit_question_result.id,
        rating='approved',
    )

    add_feedback_result = await qaf_service.add_feedback(
        project_admin_user,
        payload,
        submit_question_result.id,
        conversation_service
    )

    assert add_feedback_result is not None, "No question returned"
    assert add_feedback_result.question.content == question, "Incorrect question in question content"
    assert add_feedback_result.errand_id == question_meta["errand_id"], "Incorrect errand_id in question errand_id"
    assert add_feedback_result.subject == question_meta["subject"], "Incorrect subject in question subject"
    assert add_feedback_result.tags == question_tag, "Incorrect tags in question tags"
    assert len(add_feedback_result.messages) == 2, "Incorrect number of messages in question messages"
    assert add_feedback_result.messages[1].feedback[
               0].rating == payload.rating, "Incorrect rating in feedback"
