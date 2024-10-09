from fai_backend.new_chat.models import ClientChatState
from fai_backend.framework import components as c
from fai_backend.phrase import phrase as _


async def chat_history_edit_view(view,
                                 chat_history: ClientChatState,
                                 submit_url: str) -> list:
    return view(
        [c.Div(components=[
            c.Div(components=[
                c.Form(
                    submit_url=submit_url,
                    method='PATCH',
                    submit_text=_('update_chat_history_title_button', 'Update title'),
                    components=[
                        c.InputField(
                            name='title',
                            title=_('input_title_label', 'Edit title'),
                            placeholder=_('input_title_placeholder', f'Enter new title here'),
                            required=True,
                            html_type='text',
                        ),
                        c.InputField(
                            name='chat_id',
                            value=chat_history.chat_id,
                            hidden=True,
                            html_type='hidden',
                        )
                    ],
                )
            ], class_name='card-body'),
        ], class_name='card')],
        _('edit_chat_history_title', 'Chat history - Edit') + f' ({chat_history.title})',
    )
