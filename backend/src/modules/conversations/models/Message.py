from pydantic import BaseModel


class Message(BaseModel):
    id: str | None = None
    timestamp: str
    role: str
    content: str | None = None
    reasoning_content: str | None = None

    tool_call_id: str | None = None
    '''
    This message is a response to the following tool call.
    '''

    tool_calls: list[dict] | None = None
    '''
    This message requests the following tool calls.
    '''

    context_message_override: str | None = None
    '''
    If set this value should be used when populating messages for the context 
    instead of the actual result, for example when the tool call results in
    binary output (image etc.) that is too large for the context window.
    '''
