from fai_backend.framework import components as c
from fai_backend.phrase import phrase as _
from fai_backend.views import permission_required


@permission_required(['can_upload_document'])
def menu_items() -> list:
    return [
        c.Menu(
            title=_('documents', 'Documents'),
            id='documents-menu',
            variant='vertical',
            sub_menu=True,
            components=[
                c.Link(
                    text=_('show_all', 'Show all'),
                    url='/view/documents',
                    active='/view/documents'
                ),
                c.Link(
                    text=_('upload_new', 'Upload new'),
                    url='/view/documents/upload_form',
                    active='/view/documents/upload_form'
                ),
            ],
            icon_src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWZpbGUtdGV4dCI+PHBhdGggZD0iTTE1IDJINmEyIDIgMCAwIDAtMiAydjE2YTIgMiAwIDAgMCAyIDJoMTJhMiAyIDAgMCAwIDItMlY3WiIvPjxwYXRoIGQ9Ik0xNCAydjRhMiAyIDAgMCAwIDIgMmg0Ii8+PHBhdGggZD0iTTEwIDlIOCIvPjxwYXRoIGQ9Ik0xNiAxM0g4Ii8+PHBhdGggZD0iTTE2IDE3SDgiLz48L3N2Zz4='
        ),
    ]
