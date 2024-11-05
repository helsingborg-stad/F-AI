from typing import Optional, Any, Literal

from beanie import Document
from pydantic import BaseModel


class LLMClientChatMessage(BaseModel):
    timestamp: str
    source: str | None = None
    content: str | None = None


class AssistantStreamMessage(BaseModel):
    timestamp: str = ""
    role: str
    content: str
    should_format: bool = False


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
    max_tokens: int = -1
    allow_inline_files: bool = False
    files_collection_id: Optional[str] = None
    streams: list[AssistantStreamConfig | AssistantStreamPipelineDef]


class AssistantContext(BaseModel):
    query: str = ""
    files_collection_id: Optional[str] = None
    previous_stream_output: Optional[str] = None
    history: list[AssistantStreamMessage] = []
    rag_document: Optional[str] = None
    rag_output: Optional[str] = None


class AssistantChatHistoryModel(Document):
    user: str
    title: str = ''
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


class CountTokenRequestBody(BaseModel):
    text: str
    assistant_id: str | None = None
    conversation_id: str | None = None


class CountTokenResponseBody(BaseModel):
    count: int
