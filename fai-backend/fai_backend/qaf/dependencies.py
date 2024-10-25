from fastapi import Depends

from fai_backend.dependencies import get_project_user
from fai_backend.files.dependecies import get_file_upload_service
from fai_backend.files.service import FileUploadService
from fai_backend.llm.service import ask_llm_raq_question
from fai_backend.logger.console import console
from fai_backend.qaf.schema import (
    FeedbackPayload,
    GenerateAnswerPayload,
    QuestionDetails,
    QuestionEntry,
    QuestionFilterParams,
    SubmitAnswerPayload,
    SubmitQuestionPayload,
)
from fai_backend.qaf.service import QAFService
from fai_backend.schema import ProjectUser


async def questions_filter_params(
        q: str = None,
        tags: str = None,
        status: str = None,
        review_status: str = None,
        sort: str = None,
        sort_order: str = None,
) -> QuestionFilterParams:
    return QuestionFilterParams(
        q=q,
        tags=tags.split(',') if tags else None,
        status=status,
        review_status=review_status,
        sort=sort or 'timestamp.modified',
        sort_order=sort_order or 'desc',
    )


async def questions_loader(
        service: QAFService = Depends(QAFService.factory),
        user: ProjectUser = Depends(get_project_user),
) -> list[QuestionEntry]:
    return await service.list_submitted_questions(user)


async def filterable_questions_loader(
        service: QAFService = Depends(QAFService.factory),
        user: ProjectUser = Depends(get_project_user),
        query_params: QuestionFilterParams = Depends(questions_filter_params),
) -> list[QuestionEntry]:
    return await service.list_submitted_questions(user, query_params)


async def question_details_loader(
        conversation_id: str,
        service: QAFService = Depends(QAFService.factory),
        user: ProjectUser = Depends(get_project_user),
) -> QuestionEntry | None:
    return await service.submitted_question_details(user, conversation_id)


async def question_create_action(
        body: SubmitQuestionPayload,
        service: QAFService = Depends(QAFService.factory),
        user: ProjectUser = Depends(get_project_user),
) -> QuestionDetails:
    question = await service.submit_question(
        user,
        body.question,
        body.model_dump(exclude={'question', 'tags'}),
        body.tags,
    )

    return question


async def add_feedback_action(
        conversation_id: str,
        body: FeedbackPayload,
        service: QAFService = Depends(QAFService.factory),
        user: ProjectUser = Depends(get_project_user),
) -> QuestionDetails | None:
    return await service.add_feedback(
        user,
        body,
    )


async def add_answer_action(
        conversation_id: str,
        body: SubmitAnswerPayload,
        service: QAFService = Depends(QAFService.factory),
        user: ProjectUser = Depends(get_project_user),
) -> QuestionDetails | None:
    try:
        review = await service.add_message(
            user,
            body,
        )
        return review
    except Exception as e:
        console.log(e)
    return None


async def run_llm_on_question_create_action(
        question: QuestionDetails = Depends(question_create_action),
        service: QAFService = Depends(QAFService.factory),
        file_service: FileUploadService = Depends(get_file_upload_service),
        user: ProjectUser = Depends(get_project_user),
) -> QuestionDetails:
    latest_upload_path = file_service.get_latest_upload_path(user.project_id)
    if not latest_upload_path:
        raise Exception('No upload path found')

    directory_name = latest_upload_path.split('/')[-1]

    response = await ask_llm_raq_question(question=question.question.content, collection_name=directory_name)
    await service.add_message(
        user,
        GenerateAnswerPayload(question_id=question.id, answer=response)
    )

    return question
