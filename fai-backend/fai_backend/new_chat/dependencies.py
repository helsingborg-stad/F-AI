from fai_backend.new_chat.service import ChatStateService
from fai_backend.repositories import chat_history_repo


async def get_chat_state_service():
    return ChatStateService(chat_history_repo)
