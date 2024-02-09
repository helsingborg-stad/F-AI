from fastapi import Depends

from conversations.service import ConversationService
from dependencies import get_project_user
from fai_backend.conversations.dependencies import get_conversation_service
from fai_backend.qaf.schema import QuestionResponse, SubmitQuestionRequest
from qaf.service import QAFService
from schema import ProjectUser


def get_qaf_service(conversation_service: ConversationService = Depends(get_conversation_service)) -> QAFService:
    return QAFService(conversation_service=conversation_service)


async def create_question_request(
        body: SubmitQuestionRequest,
        user: ProjectUser = Depends(get_project_user),
        service: QAFService = Depends(get_qaf_service),
) -> QuestionResponse:
    question = await service.submit_question(user, body)
    return question


async def list_questions_request(
        user: ProjectUser = Depends(get_project_user),
        service: QAFService = Depends(get_qaf_service),
) -> list[QuestionResponse]:
    return await service.list_questions(user)
