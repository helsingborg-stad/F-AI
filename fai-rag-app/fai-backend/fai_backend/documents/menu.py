from fai_backend.framework import components as c
from fai_backend.icons import icons
from fai_backend.phrase import phrase as _
from fai_backend.views import permission_required


@permission_required(['can_upload_document'])
def menu_items() -> list:
    return [
        c.Menu(
            title=_('collections', 'Collections'),
            id='collections-menu',
            variant='vertical',
            sub_menu=True,
            icon_src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWZpbGUtdGV4dCI+PHBhdGggZD0iTTE1IDJINmEyIDIgMCAwIDAtMiAydjE2YTIgMiAwIDAgMCAyIDJoMTJhMiAyIDAgMCAwIDItMlY3WiIvPjxwYXRoIGQ9Ik0xNCAydjRhMiAyIDAgMCAwIDIgMmg0Ii8+PHBhdGggZD0iTTEwIDlIOCIvPjxwYXRoIGQ9Ik0xNiAxM0g4Ii8+PHBhdGggZD0iTTE2IDE3SDgiLz48L3N2Zz4=',
            class_name='collections-menu',
            components=[
                c.Link(
                    text=_('show_all', 'Visa alla'),
                    url='/view/collections',
                    active='/view/collections*'
                ),
                c.Link(
                    text=_('Add new Collection'),
                    url='/view/collections/create',
                    active='/view/collections/create',
                    icon_src=icons['plus'],
                ),
            ],
        )
    ]
