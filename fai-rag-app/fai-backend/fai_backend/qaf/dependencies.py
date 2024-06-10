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
    SubmitAnswerPayload,
    SubmitQuestionPayload,
)
from fai_backend.qaf.service import QAFService
from fai_backend.schema import ProjectUser


async def submit_question_request(
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


async def submit_question_and_generate_answer_request(
        question: QuestionDetails = Depends(submit_question_request),
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


async def list_my_questions_request(
        service: QAFService = Depends(QAFService.factory),
        user: ProjectUser = Depends(get_project_user),
) -> list[QuestionEntry]:
    try:
        return await service.my_questions(user)
    except Exception as e:
        console.log(e)
    return []


async def my_question_details_request(
        conversation_id: str,
        user: ProjectUser = Depends(get_project_user),
        service: QAFService = Depends(QAFService.factory),
) -> QuestionDetails | None:
    return await service.my_question_details(user, conversation_id)


async def submitted_questions_request(
        service: QAFService = Depends(QAFService.factory),
        user: ProjectUser = Depends(get_project_user),
) -> list[QuestionEntry]:
    return await service.submitted_questions(user)


async def submitted_question_details_request(
        conversation_id: str,
        service: QAFService = Depends(QAFService.factory),
        user: ProjectUser = Depends(get_project_user),
) -> QuestionEntry | None:
    return await service.submitted_question_details(user, conversation_id)


async def submit_feedback_request(
        body: FeedbackPayload,
        service: QAFService = Depends(QAFService.factory),
        user: ProjectUser = Depends(get_project_user),
) -> QuestionDetails | None:
    return await service.add_feedback(
        user,
        body,
    )


async def submit_answer_request(
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
