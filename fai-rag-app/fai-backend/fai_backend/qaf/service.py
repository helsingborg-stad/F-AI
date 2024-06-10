from fai_backend.conversations.models import Conversation, Feedback, Message
from fai_backend.logger.console import console
from fai_backend.qaf.schema import (
    ApproveAnswerPayload,
    GenerateAnswerPayload,
    QuestionDetails,
    QuestionEntry,
    RejectAnswerPayload,
    SubmitAnswerPayload,
)
from fai_backend.repositories import ConversationRepository, conversation_repo
from fai_backend.schema import ProjectUser
from fai_backend.utils import try_get_first_match


def user_can_submit_question(project_user: ProjectUser) -> bool:
    return all(permission in [key for key, value in project_user.permissions.items() if value] for permission in
               ['can_ask_questions'])


class QAFService:
    conversations: ConversationRepository

    def __init__(self, conversations: ConversationRepository):
        self.conversations = conversations

    async def submit_question(
            self,
            project_user: ProjectUser,
            question: str,
            meta: dict,
            tags: list[str] | None = None,
    ) -> QuestionDetails:
        conversation = await self.conversations.create(
            Conversation(
                id='temp_id',
                created_by=project_user.email,
                participants=[project_user.email],
                type='question',
                messages=[
                    Message(
                        user='user',
                        created_by=project_user.email,
                        content=question,
                        type='question'
                    )
                ],
                metadata=meta,
                tags=tags
            )
        )

        return QuestionDetails(**conversation.model_dump()) if conversation else None

    async def my_questions(self, project_user: ProjectUser) -> list[QuestionEntry]:
        return [QuestionEntry(**conversation.model_dump()) for conversation in await self.conversations.list() if
                conversation.type == 'question' and project_user.email in conversation.created_by]

    async def my_question_details(self, project_user: ProjectUser, question_id: str) -> QuestionDetails | None:
        conversation = await self.conversations.get(question_id)
        if conversation and conversation.created_by != project_user.email:
            raise PermissionError('User does not have permission to view this question')
        return QuestionDetails(**conversation.model_dump()) if conversation else None

    async def submitted_questions(self, project_user: ProjectUser) -> list[QuestionEntry]:
        return [QuestionEntry(**conversation.model_dump()) for conversation in await self.conversations.list() if
                conversation.type == 'question' and project_user.email in conversation.created_by]

    async def submitted_question_details(self, project_user: ProjectUser,
                                         question_id: str) -> QuestionDetails | None:
        conversation = await self.conversations.get(question_id)
        if conversation.created_by != project_user.email:
            raise PermissionError('User does not have permission to view this question')
        return QuestionDetails(**conversation.model_dump()) if conversation else None

    async def add_message(self, project_user: ProjectUser,
                          payload: SubmitAnswerPayload | GenerateAnswerPayload) -> QuestionDetails | None:
        try:
            conversation = (await self.conversations.get(payload.question_id)).model_copy()

            {
                'user': lambda: conversation.messages.append(
                    Message(
                        user='user',
                        content=payload.answer,
                        type='answer',
                        created_by=project_user.email
                    )
                ),
                'assistant': lambda: conversation.messages.append(
                    Message(
                        user='assistant',
                        content=payload.answer,
                        type='generated_answer',
                        created_by=project_user.email
                    )
                )
            }['assistant' if isinstance(payload, GenerateAnswerPayload) else 'user']()

            result = await self.conversations.update(str(conversation.id), {'messages': conversation.messages})
            return QuestionDetails(**result.model_dump())
        except Exception:
            console.print_exception(show_locals=False)

    async def add_feedback(self, project_user: ProjectUser,
                           payload: ApproveAnswerPayload | RejectAnswerPayload) -> QuestionDetails | None:
        try:
            conversation = (await self.conversations.get(payload.question_id)).model_copy()
            answer = try_get_first_match(
                conversation.messages,
                lambda message: message.type == 'generated_answer' and len(message.feedback) == 0
            )

            if answer is None:
                raise ValueError('Answer not found')

            answer.feedback.append(
                Feedback(
                    user=project_user.email,
                    created_by=project_user.email,
                    rating=payload.rating,
                    comment=payload.comment
                )
            )

            result = await self.conversations.update(str(conversation.id), {'messages': conversation.messages})
            return QuestionDetails(**result.model_dump())
        except Exception:
            console.print_exception(show_locals=False)
            raise

    @staticmethod
    def factory() -> 'QAFService':
        return QAFService(conversations=conversation_repo)
