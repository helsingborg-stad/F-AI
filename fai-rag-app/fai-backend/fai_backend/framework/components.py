from typing import Annotated, Literal

from pydantic import BaseModel, Field

__all__ = (
    'UIComponent',
    'Div',
    'Page',
    'Heading',
    'Button',
    'FireEvent',
    'Form',
    'InputField',
    'AppShell',
    'AppDrawer',
    'AppContent',
    'AppFooter',
    'PageHeader',
    'PageContent',
    'Menu',
    'Link',

    # then `AnyComponent` itself
    'AnyUI',
)

from fai_backend.framework import events as e


class UIComponent(BaseModel, extra='forbid'):
    type: str
    id: str | None = None
    class_name: str | None = Field(None, serialization_alias='class')
    components: 'list[AnyUI] | None' = None
    slot: str | None = None


class Div(UIComponent):
    type: Literal['Div'] = 'Div'


class Heading(UIComponent):
    type: Literal['Heading'] = 'Heading'
    level: Literal[1, 2, 3, 4, 5, 6] = 1
    text: str
    icon: str | None = None
    icon_state: Literal[
                    'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = Field(
        False, serialization_alias='iconState')
    badge: str | int | None = None
    badge_state: Literal[
                     'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = Field(
        False, serialization_alias='badgeState')


class Button(UIComponent):
    type: Literal['Button'] = 'Button'
    label: str
    html_type: Literal['submit', 'button'] = 'button'
    class_name: str | None = Field(None, serialization_alias='class')
    icon_src: str | None = Field(None, serialization_alias='iconSrc')
    icon_state: Literal[
                    'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = Field(
        None, serialization_alias='iconState')
    badge: str | int | None = None
    badge_state: Literal[
                     'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = Field(
        None, serialization_alias='badgeState')
    block: bool = False


class Form(BaseModel):
    submit_url: str = Field(None, serialization_alias='action')
    type: Literal['Form'] = 'Form'
    class_name: str | None = Field(None, serialization_alias='class')
    components: 'list[AnyUI]'
    method: Literal['POST', 'GET']
    submit_text: str | None = None


class InputField(BaseModel):
    type: Literal['InputField'] = 'InputField'
    name: str
    title: str | None = None
    placeholder: str | None = None
    required: bool | None = None
    html_type: Literal['text', 'password', 'hidden', 'number', 'email', 'tel'] = 'text'
    initial: str | None = Field(None, serialization_alias='value')
    hidden: bool = None
    class_name: str | None = Field(None, serialization_alias='class')
    autocomplete: str | None = None
    readonly: bool | None = None
    input_state: Literal[
                     'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = None


class Page(UIComponent):
    type: Literal['Page'] = 'Page'
    components: 'list[AnyUI]'


class FireEvent(UIComponent):
    type: Literal['FireEvent'] = 'FireEvent'
    event: 'e.AnyEvent'


class AppShell(UIComponent):
    type: Literal['AppShell'] = 'AppShell'
    hasDrawer: bool | None = None


class AppDrawer(UIComponent):
    type: Literal['AppDrawer'] = 'AppDrawer'
    title: str | None = None


class Menu(UIComponent):
    type: Literal['Menu'] = 'Menu'
    title: str | None = None
    variant: Literal['vertical', 'horizontal'] = 'vertical'
    sub_menu: bool = Field(False, serialization_alias='subMenu')
    size: Literal['xs', 'sm', 'md', 'lg'] | None = None


class Link(UIComponent):
    type: Literal['Link'] = 'Link'
    title: str
    url: str | None = Field(None, serialization_alias='href')
    state: Literal['primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success'] | None = None
    underline: Literal['on-hover', 'always', 'never'] | bool | None = None
    active: bool = False
    icon: str | None = Field(
        None, serialization_alias='iconSrc')
    icon_state: Literal[
                    'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = Field(
        False, serialization_alias='iconState')
    badge: str | int | None = None
    badge_state: Literal[
                     'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = Field(
        False, serialization_alias='badgeState')


class AppContent(UIComponent):
    type: Literal['AppContent'] = 'AppContent'


class PageHeader(UIComponent):
    type: Literal['PageHeader'] = 'PageHeader'
    fixed: bool = False


class PageContent(UIComponent):
    type: Literal['PageContent'] = 'PageContent'


class AppFooter(UIComponent):
    type: Literal['AppFooter'] = 'AppFooter'


AnyUI = Annotated[
    (Div | Form | InputField | Button | FireEvent | Heading | Page |
     AppShell | AppDrawer | AppContent | AppFooter | PageHeader |
     PageContent | Menu | Link),
    Field(discriminator='type')
]
