from fai_backend.framework import components as c
from fai_backend.views import permission_required
from fai_backend.icons import icons
from fai_backend.phrase import phrase as _


@permission_required(['can_ask_questions'])
def menu_items() -> list:
    return [
        c.Menu(
            title=_('chat', 'Chat'),
            id='chat-menu',
            variant='vertical',
            sub_menu=True,
            components=[
                c.Link(
                    text=_('start_new_chat', 'Start new'),
                    url='/chat',
                    active='/chat'
                ),
                c.Link(
                    text=_('chat_history', 'Chat history'),
                    url='/chat/history'
                ),
            ],
            icon_src=icons['chat_bot']
        )
    ]
