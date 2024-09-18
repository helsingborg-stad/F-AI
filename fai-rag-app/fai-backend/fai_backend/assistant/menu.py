from fai_backend.framework import components as c
from fai_backend.icons import icons
from fai_backend.phrase import phrase as _
from fai_backend.views import permission_required


@permission_required(['can_edit_questions_and_answers'])
def assistant_menu() -> list:
    return [
        c.Menu(
            title=_('Assistant'),
            id='assistants-menu',
            variant='vertical',
            sub_menu=True,
            icon_src=icons['assistant'],
            class_name='assistants-menu',
            components=[
                c.Link(
                    text=_('show_all', 'Visa alla'),
                    url='/assistants',
                    active='/assistants*'
                ),
                c.Link(
                    text=_('Add new Assistant'),
                    url='/assistants/create',
                    active='/assistants/create',
                    icon_src=icons['plus'],
                ),
            ],
        ),
    ]
