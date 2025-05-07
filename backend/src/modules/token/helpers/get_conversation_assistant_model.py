from typing import Tuple

from src.modules.assistants.models.Assistant import Assistant
from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.conversations.models.Conversation import Conversation
from src.modules.conversations.protocols.IConversationService import IConversationService
from src.modules.llm.helpers.parse_model_key import parse_model_key


async def get_conversation_assistant_model(
        as_uid: str,
        assistant_service: IAssistantService,
        conversation_service: IConversationService,
        conversation_id: str
) -> Tuple[Conversation, Assistant, str] | None:
    conversation = await conversation_service.get_conversation(as_uid=as_uid, conversation_id=conversation_id)

    if not conversation:
        return None

    assistant = await assistant_service.get_assistant(as_uid=as_uid, assistant_id=conversation.assistant_id,
                                                      redact_key=False)

    if not assistant:
        return None

    _, model_name = parse_model_key(assistant.model)

    return conversation, assistant, model_name
