


from typing import Any, Callable, Dict, List, Optional, TypeVar
from backend.server.db.repository import Repository, create_repository
from backend.server.schema.conversation.input import InputConversation, InputFeedback, InputMessage
from backend.server.schema.conversation.response import OutputConversation
from ..db.model.conversation import ConversationModel, ConversationRepositoryModel, InsertConversationModel, InsertFeedbackModel
from rich.pretty import pprint

T = TypeVar('T')


Condition = Callable[[T], bool]


def conversation_exists() -> Condition[Optional[ConversationModel]]:
    return lambda conversation: conversation is not None


def message_exists_in_conversation(message_id: int) -> Condition[Optional[ConversationModel]]:
    return lambda conversation: conversation and message_id < len(conversation.messages)


def feedback_does_not_exist_for_message(message_id: int) -> Condition[Optional[ConversationModel]]:
    return lambda conversation: conversation and conversation.messages[message_id] and len(conversation.messages[message_id].feedback) == 0


def all_conditions_met(conditions: List[Condition[T]]) -> Condition[T]:
    def check_conditions(item: T) -> bool:
        for condition in conditions:
            if not condition(item):
                return False
        return True
    return check_conditions


def can_add_feedback(conversation: ConversationModel, message_id: str)->bool:
    conditions = all_conditions_met([
        conversation_exists(),
        message_exists_in_conversation(message_id),
        feedback_does_not_exist_for_message(message_id),
    ])
    
    return conditions(conversation)


class ConversationService():
    conversations: ConversationRepositoryModel
    def __init__(self, conversations: ConversationRepositoryModel):
        self.conversations = conversations
        
    async def create_conversation(self, input: InputConversation, user: str)->OutputConversation:
        result = await self.conversations.insert(InsertConversationModel(messages=input.messages, created_by=user, participants=[user]))
        return OutputConversation.parse_raw(result.json())

    async def find_by_id(self, conversation_id: str)->OutputConversation:
        result = await self.conversations.find_by_id(conversation_id)
        return OutputConversation.parse_raw(result.json())

    async def find_all(self, q: Dict[str, Any] = {})->List[OutputConversation]:
        result = await self.conversations.find_all()
        return [OutputConversation.parse_raw(conversation.json()) for conversation in result]

    async def add_messages(self, conversation_id: str, input_messages: List[InputMessage])->OutputConversation:
        result = await self.conversations.insert_message(conversation_id, input_messages)
        return OutputConversation.parse_raw(result.json())
    
    async def add_feedback(self, conversation_id: str, message_id: str, input_feedback: InputFeedback, user: str)->OutputConversation:
        conversation = await self.conversations.find_by_id(conversation_id)
        pprint(can_add_feedback(conversation, message_id))
        if conversation and can_add_feedback(conversation, message_id):
            result = await self.conversations.insert_feedback(
                conversation_id, 
                message_id, 
                InsertFeedbackModel(user=user, **input_feedback.dict())
            )

            return OutputConversation.parse_raw(result.json())
        else:
            raise Exception("Cannot add feedback")

def conversation_service_factory(repository_factory: Callable[[], Repository] = create_repository)->Callable[[], ConversationService]:
    def create_conversation_service()->ConversationService:
        return ConversationService(repository_factory().conversations)

    return create_conversation_service

create_conversation_service = conversation_service_factory()