from typing import Optional, Any, Literal

from beanie import Document
from pydantic import BaseModel

from fai_backend.repository.interface import IAsyncRepo


class LLMClientChatMessage(BaseModel):
    timestamp: str
    source: str | None = None
    content: str | None = None


class ToolCallFunction(BaseModel):
    name: str
    arguments: str


class ToolCall(BaseModel):
    id: str
    type: Literal["function"]
    function: ToolCallFunction


class AssistantStreamMessage(BaseModel):
    timestamp: str = ""
    role: str
    content: str
    should_format: bool = False
    tool_call_id: Optional[str] = None
    tool_calls: Optional[list[ToolCall]] = None


class AssistantStreamInsert(BaseModel):
    insert: str


class AssistantStreamConfig(BaseModel):
    provider: str
    settings: dict[str, Any]
    messages: list[AssistantStreamMessage | AssistantStreamInsert]


class AssistantStreamPipelineDef(BaseModel):
    pipeline: str


class AssistantTemplateMeta(BaseModel):
    name: str = ""
    description: str = ""
    sample_questions: list[str] = []


class AssistantTemplate(BaseModel):
    id: str
    meta: AssistantTemplateMeta
    files_collection_id: Optional[str] = None
    streams: list[AssistantStreamConfig | AssistantStreamPipelineDef]


class ClientChatState(BaseModel):
    user: str
    chat_id: str
    timestamp: str
    title: str
    delete_label: str = "Delete"  # TODO: fix hack for allowing something to show up in list to click on.
    history: list[LLMClientChatMessage]


class AssistantChatHistoryModel(Document):
    user: str
    assistant: AssistantTemplate
    history: list[AssistantStreamMessage] = []

    class Settings:
        name = 'chat_history'
        use_state_management = True


class StoredQuestionModel(Document):
    question: str
    user: str

    class Settings:
        name = 'stored_questions'
        use_state_management = True


class AssistantContext(BaseModel):
    conversation_id: str = ""
    query: str = ""
    files_collection_id: Optional[str] = None
    previous_stream_output: Optional[str] = None
    history: list[AssistantStreamMessage] = []
    rag_output: Optional[str] = None

    async def add_to_history(self, new_messages: list[AssistantStreamMessage],
                             repo: IAsyncRepo[AssistantChatHistoryModel]):
        new_history = await repo.get(self.conversation_id)
        for message in new_messages:
            new_history.history.append(message)
        await repo.update(self.conversation_id, new_history.model_dump(exclude={'id'}))
        self.history = new_history.history
