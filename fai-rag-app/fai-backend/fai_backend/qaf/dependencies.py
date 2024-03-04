from fastapi import Depends

from fai_backend.dependencies import get_project_user
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
from llm.service import ask_llm_raq_question


async def submit_question_request(
        body: SubmitQuestionPayload,
        service: QAFService = Depends(QAFService.factory),
        user: ProjectUser = Depends(get_project_user),
) -> QuestionDetails:
    question = await service.submit_question(
        user,
        body.question,
        body.model_dump(exclude={'question'}),
    )

    return question


async def submit_question_and_generate_answer_request(
        question: QuestionDetails = Depends(submit_question_request),
        service: QAFService = Depends(QAFService.factory),
        user: ProjectUser = Depends(get_project_user),
) -> QuestionDetails:
    response = await ask_llm_raq_question(question.question.content)
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
