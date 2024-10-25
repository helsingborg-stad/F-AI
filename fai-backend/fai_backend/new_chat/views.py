from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.framework.display import DisplayAs
from fai_backend.framework.table import DataColumn
from fai_backend.new_chat.models import ClientChatState
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
                            placeholder=_('input_title_placeholder', 'Enter new title here'),
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
        _('edit_chat_history_title', f'Chat history - Edit ({chat_history.title})'),
    )


async def chat_history_list_view(view, states: list[ClientChatState]) -> list:
    return view(
        [c.DataTable(data=states,
                     columns=[DataColumn(key='title',
                                         id='title',
                                         width=100,
                                         display=DisplayAs.link,
                                         on_click=e.GoToEvent(url='/chat/{chat_id}'),
                                         sortable=True,
                                         label=_('title', 'Title')),
                              DataColumn(key='rename_label',
                                         display=DisplayAs.link,
                                         on_click=e.GoToEvent(url='/chat/edit/{chat_id}'),
                                         label=_('actions', 'Action')),
                              DataColumn(key='delete_label',
                                         width=1,
                                         display=DisplayAs.link,
                                         on_click=e.GoToEvent(url='/chat/delete/{chat_id}'),
                                         label=_('actions', 'Action'))],
                     include_view_action=False)],
        _('chat_history', 'Chat history')
    )
