from pydantic import BaseModel


class ToolCallResult(BaseModel):
    result: str

    context_message_override: str | None = None
    '''
    If set this value should be used when populating messages for the context 
    instead of the actual result, for example when the tool call results in
    binary output (image etc.) that is too large for the context window.
    '''