from dataclasses import dataclass
from pydantic import BaseModel
from .model.conversation import ConversationRepositoryModel
from .mongodb_conversation import ConversationRepository as MongoConversationRepository

@dataclass
class Repository():
    conversations: ConversationRepositoryModel
    
def create_repository()->Repository:
    return Repository(
        conversations=MongoConversationRepository(),
    )