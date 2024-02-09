from conversations.schema import CreateConversationRequest, CreateMessageRequest
from conversations.service import ConversationService
from fai_backend.qaf.schema import QuestionResponse, SubmitQuestionRequest
from schema import ProjectUser
from utils import try_get_first_match


def user_can_submit_question(project_user: ProjectUser) -> bool:
    return all(permission in [key for key, value in project_user.permissions.items() if value] for permission in
               ['can_ask_questions'])


class QAFService:
    conversation_service: ConversationService

    def __init__(self, conversation_service: ConversationService):
        self.conversation_service = conversation_service

    async def submit_question(
            self,
            project_user: ProjectUser,
            payload: SubmitQuestionRequest
    ) -> QuestionResponse | None:
        try:
            if not user_can_submit_question(project_user):
                raise PermissionError('User does not have permission to submit a question')

            new_conversation = await self.conversation_service.create_conversation(
                project_user.email,
                CreateConversationRequest(
                    project_id=project_user.project_id,
                    messages=[
                        CreateMessageRequest(
                            user=project_user.email,
                            content=payload.question,
                            type='question'
                        )
                    ],
                    metadata={
                        'subject': payload.subject,
                        'errand_id': payload.errand_id
                    }
                )
            )

            if new_conversation is None:
                raise ValueError('Failed to submit question')

            return QuestionResponse(
                id=new_conversation.id,
                question=new_conversation.messages[0].content,
                subject=new_conversation.metadata['subject'],
                errand_id=new_conversation.metadata['errand_id'],
                created_by=new_conversation.created_by,
                answer=''
            )

        except Exception as e:
            raise e

    async def list_questions(self, project_user: ProjectUser) -> list[QuestionResponse]:
        try:
            return [QuestionResponse(
                id=conversation.id,
                question=conversation.messages[0].content,
                subject=conversation.metadata['subject'],
                errand_id=conversation.metadata['errand_id'],
                created_by=conversation.created_by,
                answer=''
            ) for conversation in [*await self.conversation_service.list_conversations()] if
                conversation.created_by == project_user.email]
        except Exception as e:
            raise e

    async def get_question(self, project_user: ProjectUser, question_id: str) -> QuestionResponse:
        try:
            conversation = await self.conversation_service.get_conversation_by_id(question_id)
            if conversation is None:
                raise ValueError('Question not found')

            if conversation.created_by != project_user.email:
                raise PermissionError('User does not have permission to view this question')

            if conversation.messages[0].type != 'question':
                raise ValueError('Conversation type is not a question')

            answer = try_get_first_match(
                conversation.messages,
                lambda message:
                message.type == 'generated_answer'
                and try_get_first_match(
                    message.feedback or [],
                    lambda feedback:
                    feedback.rating == 'approved')
                is not None
            )

            answer = answer if answer is not None else try_get_first_match(
                conversation.messages,
                lambda message: message.type == 'answer'
            )

            return QuestionResponse(
                id=conversation.id,
                question=conversation.messages[0].content,
                subject=conversation.metadata['subject'],
                errand_id=conversation.metadata['errand_id'],
                created_by=conversation.created_by,
                answer=answer if answer is not None else ''
            )
        except Exception as e:
            raise e
