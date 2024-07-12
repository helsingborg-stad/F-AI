from fai_backend.conversations.models import Message, Conversation
from fai_backend.repositories import ConversationRepository
from fai_backend.repository.query.component import LogicalExpression, AttributeAssignment


async def get_root_conversations_created_by_user(
        conversation_repo: ConversationRepository,
        user_email: str
) -> list[Conversation]:
    active_conversation_by_user = LogicalExpression('AND', [
        AttributeAssignment('conversation_root_id', None),
        AttributeAssignment('created_by', user_email)
    ])

    return await conversation_repo.list(active_conversation_by_user)


def get_first_message_in_conversation(
        conversation: Conversation
) -> list[Message]:
    return [conversation.messages[0]] if conversation.messages else []


def get_last_message_in_conversation(
        conversation: Conversation
) -> list[Message]:
    return [conversation.messages[-1]] if conversation.messages else []


def get_all_messages_in_conversation(
        conversation: Conversation
) -> list[Message]:
    return conversation.messages
