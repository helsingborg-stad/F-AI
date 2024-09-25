from fai_backend.framework import components as c
from fai_backend.phrase import phrase as _


def menu_items() -> list:
    return [
        c.Link(
            text=_('give_feedback', 'Send Feedback'),
            url='/feedback',
            active='/feedback',
        ),
    ]
