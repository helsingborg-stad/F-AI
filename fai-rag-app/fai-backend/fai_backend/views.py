from fai_backend.documents.menu import menu_items as document_menu_items
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


def reviewer_menu() -> list:
    return [
        c.Menu(
            title=_('reviews', 'Reviews'),
            id='reviewer-menu',
            variant='vertical',
            components=[
                c.Link(
                    text=_('inbox', 'Inbox'),
                    url='/reviews',
                    badge='3',
                    badge_state='accent',
                )
            ]
        ),
    ]


def mock_menu() -> list:
    return [
        c.Menu(
            id='mock-menu',
            variant='vertical',

            components=[

                c.Link(
                    text=_('assistant', 'Assistant'),
                    url='/',
                    icon_src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWJyYWluLWNpcmN1aXQiPjxwYXRoIGQ9Ik0xMiA0LjVhMi41IDIuNSAwIDAgMC00Ljk2LS40NiAyLjUgMi41IDAgMCAwLTEuOTggMyAyLjUgMi41IDAgMCAwLTEuMzIgNC4yNCAzIDMgMCAwIDAgLjM0IDUuNTggMi41IDIuNSAwIDAgMCAyLjk2IDMuMDggMi41IDIuNSAwIDAgMCA0LjkxLjA1TDEyIDIwVjQuNVoiLz48cGF0aCBkPSJNMTYgOFY1YzAtMS4xLjktMiAyLTIiLz48cGF0aCBkPSJNMTIgMTNoNCIvPjxwYXRoIGQ9Ik0xMiAxOGg2YTIgMiAwIDAgMSAyIDJ2MSIvPjxwYXRoIGQ9Ik0xMiA4aDgiLz48cGF0aCBkPSJNMjAuNSA4YS41LjUgMCAxIDEtMSAwIC41LjUgMCAwIDEgMSAwWiIvPjxwYXRoIGQ9Ik0xNi41IDEzYS41LjUgMCAxIDEtMSAwIC41LjUgMCAwIDEgMSAwWiIvPjxwYXRoIGQ9Ik0yMC41IDIxYS41LjUgMCAxIDEtMSAwIC41LjUgMCAwIDEgMSAwWiIvPjxwYXRoIGQ9Ik0xOC41IDNhLjUuNSAwIDEgMS0xIDAgLjUuNSAwIDAgMSAxIDBaIi8+PC9zdmc+'
                ),
                *document_menu_items(),
                c.Link(
                    text=_('metrics', 'Metrics'),
                    url='/',
                    icon_src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWJhci1jaGFydC0zIj48cGF0aCBkPSJNMyAzdjE4aDE4Ii8+PHBhdGggZD0iTTE4IDE3VjkiLz48cGF0aCBkPSJNMTMgMTdWNSIvPjxwYXRoIGQ9Ik04IDE3di0zIi8+PC9zdmc+'
                ),
                c.Link(
                    text=_('users', 'Users'),
                    url='/',
                    icon_src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXVzZXJzLXJvdW5kIj48cGF0aCBkPSJNMTggMjFhOCA4IDAgMCAwLTE2IDAiLz48Y2lyY2xlIGN4PSIxMCIgY3k9IjgiIHI9IjUiLz48cGF0aCBkPSJNMjIgMjBjMC0zLjM3LTItNi41LTQtOGE1IDUgMCAwIDAtLjQ1LTguMyIvPjwvc3ZnPg=='
                )

            ]
        ),
    ]


def app_drawer() -> list:
    return [
        c.AppDrawer(
            title='Folkets AI',
            components=[
                *questions_menu(),
                *reviewer_menu(),
                *mock_menu(),
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
            class_name='flex-1 lg:flex-none font-semibold text-base-content',
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
