from mistral_common.protocol.instruct.request import ChatCompletionRequest
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.messages import SystemMessage, UserMessage, AssistantMessage

from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.conversations.models.Message import Message
from src.modules.conversations.protocols.IConversationService import IConversationService
from src.modules.llm.helpers.parse_model_key import parse_model_key
from src.modules.token.helpers.get_conversation_assistant_model import get_conversation_assistant_model
from src.modules.token.protocols.ITokenService import ITokenService


class MistralTokenService(ITokenService):
    def __init__(self, assistant_service: IAssistantService, conversation_service: IConversationService):
        self._assistant_service = assistant_service
        self._conversation_service = conversation_service

    async def get_token_count(self, as_uid: str, assistant_id: str, message: str) -> int:
        assistant = await self._assistant_service.get_assistant(as_uid=as_uid, assistant_id=assistant_id,
                                                                redact_key=False)

        if not assistant:
            return -1

        [_, model_name] = parse_model_key(assistant.model)

        tokenizer = MistralTokenizer.from_model(model_name)

        tokenized = tokenizer.encode_chat_completion(ChatCompletionRequest(
            messages=[
                SystemMessage(content=assistant.instructions),
                UserMessage(content=message)
            ],
            model=model_name,
        ))

        return len(tokenized.tokens)

    async def get_token_count_with_history(self, as_uid: str, conversation_id: str, message: str) -> int:
        fetched = await get_conversation_assistant_model(
            as_uid=as_uid,
            assistant_service=self._assistant_service,
            conversation_service=self._conversation_service,
            conversation_id=conversation_id
        )

        if not fetched:
            return -1

        conversation, assistant, model_name = fetched

        tokenizer = MistralTokenizer.from_model(model_name)

        tokenized = tokenizer.encode_chat_completion(ChatCompletionRequest(
            messages=[self._to_mistral_message(m) for m in conversation.messages]
                     + [UserMessage(content=message)],
            model=model_name,
        ))

        return len(tokenized.tokens)

    @staticmethod
    def _to_mistral_message(message: Message) -> SystemMessage | AssistantMessage | UserMessage:
        match message.role:
            case 'system':
                return SystemMessage(content=message.content)
            case 'assistant':
                return AssistantMessage(content=message.content)
            case _:
                return UserMessage(content=message.content)
