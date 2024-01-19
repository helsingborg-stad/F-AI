from fai_backend.framework import components as c
from fai_backend.phrase import phrase as _


def page_template(*components, page_title: str = None) -> list:
    def page_title_component() -> list:
        return [c.Heading(
            text=page_title,
            class_name='flex-none',
        )] if page_title else []

    return [
        c.AppShell(
            hasDrawer=True,
            components=[
                c.AppDrawer(
                    slot='drawer',
                    title='Folkets AI',
                    components=[
                        c.Menu(
                            title=_('questions', 'Questions'),
                            id='questions-menu',
                            variant='vertical',
                            components=[
                                c.Link(
                                    title=_('submit_question', 'Submit a question'),
                                    url='/',
                                ),
                                c.Menu(
                                    title=_('my_questions', 'My Questions'),
                                    id='questions-menu',
                                    variant='vertical',
                                    sub_menu=True,
                                    components=[
                                        c.Link(
                                            title=_('show_all', 'Visa alla'),
                                            url='/questions'
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ]
                ),
                c.AppContent(
                    components=[
                        c.PageHeader(
                            fixed=True,
                            components=[
                                *page_title_component(),
                                c.Menu(
                                    id='toolbar-menu',
                                    variant='horizontal',
                                    class_name='flex flex-row flex-1 justify-end',
                                    components=[
                                        c.Link(
                                            title=_('logout_button_text', 'Logout'),
                                            url='/logout',
                                            icon='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWxvZy1vdXQiPjxwYXRoIGQ9Ik05IDIxSDVhMiAyIDAgMCAxLTItMlY1YTIgMiAwIDAgMSAyLTJoNCIvPjxwb2x5bGluZSBwb2ludHM9IjE2IDE3IDIxIDEyIDE2IDciLz48bGluZSB4MT0iMjEiIHgyPSI5IiB5MT0iMTIiIHkyPSIxMiIvPjwvc3ZnPg=='
                                        ),
                                    ],
                                ),
                            ]
                        ),
                        c.PageContent(
                            class_name='mt-24',
                            components=[
                                *components,
                            ]
                        ),
                        c.AppFooter(
                            components=[
                                c.Heading(
                                    text='folketsAi',
                                ),
                            ]
                        )
                    ],
                ),
            ],
        )
    ]
