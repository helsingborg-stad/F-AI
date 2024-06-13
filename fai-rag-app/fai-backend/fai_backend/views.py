from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar, cast

from fai_backend.framework import components as c
from fai_backend.icons import icons
from fai_backend.phrase import phrase as _

T = TypeVar('T', bound=Callable[..., list[Any]])


def permission_required(required_permissions: list[str]) -> Callable[[T], T]:
    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            user_permissions = kwargs.get('user_permissions', [])

            if not user_permissions:
                user_permissions = []

            if user_permissions:
                kwargs.pop('user_permissions')

            if not required_permissions or all(
                    (permission in user_permissions) for permission in required_permissions
            ):
                return func(*args, **kwargs)
            else:
                return []

        return cast(T, wrapper)

    return decorator


@permission_required(['can_ask_questions'])
def chat_menu() -> list:
    return [
        c.Link(
            text=_('chat', 'Chat'),
            url='/chat',
            icon_src=icons['message_square_more'],
            active='/chat*'
        )
    ]


@permission_required(['can_edit_questions_and_answers'])
def mock_menu() -> list:
    return [
        c.Link(
            text=_('assistant', 'Assistant'),
            url='#',
            disabled=True,
            icon_src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWJyYWluLWNpcmN1aXQiPjxwYXRoIGQ9Ik0xMiA0LjVhMi41IDIuNSAwIDAgMC00Ljk2LS40NiAyLjUgMi41IDAgMCAwLTEuOTggMyAyLjUgMi41IDAgMCAwLTEuMzIgNC4yNCAzIDMgMCAwIDAgLjM0IDUuNTggMi41IDIuNSAwIDAgMCAyLjk2IDMuMDggMi41IDIuNSAwIDAgMCA0LjkxLjA1TDEyIDIwVjQuNVoiLz48cGF0aCBkPSJNMTYgOFY1YzAtMS4xLjktMiAyLTIiLz48cGF0aCBkPSJNMTIgMTNoNCIvPjxwYXRoIGQ9Ik0xMiAxOGg2YTIgMiAwIDAgMSAyIDJ2MSIvPjxwYXRoIGQ9Ik0xMiA4aDgiLz48cGF0aCBkPSJNMjAuNSA4YS41LjUgMCAxIDEtMSAwIC41LjUgMCAwIDEgMSAwWiIvPjxwYXRoIGQ9Ik0xNi41IDEzYS41LjUgMCAxIDEtMSAwIC41LjUgMCAwIDEgMSAwWiIvPjxwYXRoIGQ9Ik0yMC41IDIxYS41LjUgMCAxIDEtMSAwIC41LjUgMCAwIDEgMSAwWiIvPjxwYXRoIGQ9Ik0xOC41IDNhLjUuNSAwIDEgMS0xIDAgLjUuNSAwIDAgMSAxIDBaIi8+PC9zdmc+'
        ),
        c.Link(
            text=_('users', 'Users'),
            url='/users',
            active='/users*',
            icon_src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXVzZXJzLXJvdW5kIj48cGF0aCBkPSJNMTggMjFhOCA4IDAgMCAwLTE2IDAiLz48Y2lyY2xlIGN4PSIxMCIgY3k9IjgiIHI9IjUiLz48cGF0aCBkPSJNMjIgMjBjMC0zLjM3LTItNi41LTQtOGE1IDUgMCAwIDAtLjQ1LTguMyIvPjwvc3ZnPg=='
        )
    ]


def app_drawer(menus: list | None = None) -> list:
    return [
        c.AppDrawer(
            title='Folkets AI',
            components=[
                c.Menu(
                    components=[] if not menus else menus
                ),
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


def page_template(*components, page_title: str = None, menus: list | None = None) -> list:
    def page_title_component() -> list:
        return [c.Heading(
            text=page_title,
            class_name='flex-1 lg:flex-none font-semibold text-base-content',
        )] if page_title else []

    return [
        c.AppShell(
            hasDrawer=True,
            components=[
                *app_drawer(menus),
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
