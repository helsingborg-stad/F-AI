from typing import Literal

from pydantic import BaseModel, computed_field

from fai_backend.conversations.models import Conversation, Feedback, Message
from fai_backend.conversations.schema import ResponseMessage, CreateConversationRequest, CreateMessageRequest
from fai_backend.conversations.service import ConversationService
from fai_backend.logger.console import console
from fai_backend.qaf.schema import (
    ApproveAnswerPayload,
    GenerateAnswerPayload,
    QuestionDetails,
    QuestionEntry,
    QuestionFilterParams,
    RejectAnswerPayload,
    SubmitAnswerPayload,
)
from fai_backend.repositories import ConversationRepository, conversation_repo
from fai_backend.repository.query.component import AttributeAssignment, LogicalExpression
from fai_backend.schema import ProjectUser, Timestamp
from fai_backend.utils import try_get_first_match


def user_can_submit_question(project_user: ProjectUser) -> bool:
    return all(permission in [key for key, value in project_user.permissions.items() if value] for permission in
               ['can_ask_questions'])


class QAFService:
    conversations: ConversationRepository

    def __init__(self, conversations: ConversationRepository):
        self.conversations = conversations

    async def submit_new_question(
            self,
            conversation_service: ConversationService,
            project_user: ProjectUser,
            question: str,
            meta: dict,
            tags: list[str] | None = None,
    ) -> QuestionDetails:
        conversation = await conversation_service.create_conversation(
            project_user.email,
            CreateConversationRequest(
                project_id=project_user.project_id,
                messages=[
                    CreateMessageRequest(
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

        return self._to_question(conversation) if conversation else None

    async def list_my_questions(self, project_user: ProjectUser) -> list[QuestionEntry]:

        return [self._to_question(conversation) for conversation in
                await self.conversations.list(query=LogicalExpression('AND', [
                    AttributeAssignment('type', 'question'),
                    AttributeAssignment('created_by', project_user.email)
                ]))]

    async def my_question_details(self, project_user: ProjectUser, question_id: str) -> QuestionDetails | None:
        conversation = await self.conversations.get(question_id)
        if conversation and conversation.created_by != project_user.email:
            raise PermissionError('User does not have permission to view this question')
        return self._to_question(conversation) if conversation else None

    async def list_submitted_questions(self, project_user: ProjectUser, query_params: QuestionFilterParams) -> list[
        QuestionEntry]:

        db_query = LogicalExpression('AND', [
            AttributeAssignment('type', 'question'),
            AttributeAssignment('created_by', project_user.email)
        ])

        questions = [self._to_question(conversation) for conversation in await self.conversations.list(
            query=db_query,
            sort_by=query_params.sort,
            sort_order=query_params.sort_order
        )]

        return list(filter(lambda question: (
                (not query_params.status or question.status == query_params.status)
                and (not query_params.review_status or question.review_status == query_params.review_status)
        ), questions))

    async def submitted_question_details(self, project_user: ProjectUser, question_id: str) -> QuestionDetails | None:
        conversation = await self.conversations.get(question_id)
        if conversation.created_by != project_user.email:
            raise PermissionError('User does not have permission to view this question')
        return self._to_question(conversation) if conversation else None

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
            return self._to_question(result)
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
            return self._to_question(result)
        except Exception:
            console.print_exception(show_locals=False)
            raise

    def _to_question(self, conversation: Conversation) -> QuestionDetails:
        return QuestionDetails.model_validate({
            **conversation.model_dump(),
            **self._QuestionState(conversation=conversation).model_dump()
        })

    class _QuestionState(BaseModel):
        conversation: Conversation

        @computed_field
        def timestamp(self) -> Timestamp:
            return Timestamp(
                created=self.conversation.messages[0].timestamp.created,
                modified=self.conversation.messages[-1].timestamp.modified
            )

        @computed_field
        def subject(self) -> str:
            return self.conversation.metadata['subject']

        @computed_field
        def errand_id(self) -> str:
            return self.conversation.metadata['errand_id']

        @computed_field
        def status(self) -> Literal['open', 'pending', 'answered', 'resolved', 'closed']:
            if try_get_first_match(
                    self.conversation.messages,
                    lambda message: message.type == 'event' and message.content == 'user_closed_question'
            ):
                return 'closed'
            elif len(self.conversation.messages) == 1:
                return 'open'
            elif self.review_status == 'approved':
                return 'resolved'
            elif len(self.conversation.messages) > 1 and self.answer is None:
                return 'pending'

        @computed_field
        def review_status(self) -> Literal['approved', 'rejected', 'in-progress', 'closed', 'blocked', 'open'] | None:
            generated_answer = try_get_first_match(
                self.conversation.messages,
                lambda message: message.type == 'generated_answer'
            )

            if not generated_answer:
                return 'blocked'

            if generated_answer and len(generated_answer.feedback) == 0:
                return 'open'

            if generated_answer.feedback[0].rating == 'approved':
                return 'approved'

            if generated_answer.feedback[0].rating == 'rejected':
                if self.answer is None:
                    return 'in-progress'
                return 'rejected'

            return None

        @computed_field
        def answer(self) -> ResponseMessage | None:
            answer = try_get_first_match(
                self.conversation.messages,
                lambda message: message.type == 'answer' or
                                message.type == 'generated_answer'
                                and len(message.feedback) > 0
                                and message.feedback[0].rating == 'approved'
            )
            return ResponseMessage.model_validate(answer.model_dump()) if answer is not None else None

        @computed_field
        def question(self) -> ResponseMessage:
            return ResponseMessage.model_validate(self.conversation.messages[0].model_dump())

    @staticmethod
    def factory() -> 'QAFService':
        return QAFService(conversations=conversation_repo)
