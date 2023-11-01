from dataclasses import dataclass
from .model.conversation_repository import ConversationRepositoryModel
from .mongodb_conversation import ConversationRepository as MongoConversationRepository


@dataclass
class Repository:
    conversations: ConversationRepositoryModel


def create_repository() -> Repository:
    return Repository(
        conversations=MongoConversationRepository(),
    )
