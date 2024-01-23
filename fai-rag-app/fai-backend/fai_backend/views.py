from fai_backend.framework import components as c
from fai_backend.phrase import phrase as _


def questions_menu() -> list:
    return [
        c.Menu(
            title=_('questions', 'Questions'),
            id='questions-menu',
            variant='vertical',
            components=[
                c.Link(
                    text=_('submit_question', 'Submit a question'),
                    url='/questions/create',
                ),
                c.Menu(
                    title=_('my_questions', 'My Questions'),
                    id='questions-menu',
                    variant='vertical',
                    sub_menu=True,
                    components=[
                        c.Link(
                            text=_('show_all', 'Visa alla'),
                            url='/questions'
                        ),
                    ],
                ),
            ],
        ),
    ]


def app_drawer() -> list:
    return [
        c.AppDrawer(
            slot='drawer',
            title='Folkets AI',
            components=[
                *questions_menu(),
            ]
        )
    ]


def toolbar_menu() -> list:
    return [
        c.Div(
            class_name='flex-0 ml-auto',
            components=[
                c.Link(
                    text=_('logout_button_text', 'Logout'),
                    url='/logout',
                    class_name='btn btn-ghost font-normal',
                    icon_src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWxvZy1vdXQiPjxwYXRoIGQ9Ik05IDIxSDVhMiAyIDAgMCAxLTItMlY1YTIgMiAwIDAgMSAyLTJoNCIvPjxwb2x5bGluZSBwb2ludHM9IjE2IDE3IDIxIDEyIDE2IDciLz48bGluZSB4MT0iMjEiIHgyPSI5IiB5MT0iMTIiIHkyPSIxMiIvPjwvc3ZnPg=='
                ),
            ]
        )
    ]


def app_footer() -> list:
    return [
        c.AppFooter(
            components=[
                c.Heading(
                    text='folketsAi',
                ),
            ]
        )
    ]


def page_template(*components, page_title: str = None) -> list:
    def page_title_component() -> list:
        return [c.Heading(
            text=page_title,
            class_name='flex-1 lg:flex-none',
        )] if page_title else []

    return [
        c.AppShell(
            hasDrawer=True,
            components=[
                *app_drawer(),
                c.AppContent(
                    components=[
                        c.PageHeader(
                            components=[
                                *page_title_component(),
                                *toolbar_menu()
                            ]
                        ),
                        c.PageContent(
                            components=[
                                *components,
                            ]
                        ),
                        # *app_footer(),
                    ],
                ),
            ],
        )
    ]
