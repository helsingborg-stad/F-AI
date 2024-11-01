from typing import Annotated, Literal

from pydantic import BaseModel, Field

__all__ = (
    'Div',
    'Heading',
    'Button',
    'FireEvent',
    'Form',
    'InputField',
    'Textarea',
    'AppShell',
    'AppDrawer',
    'AppContent',
    'AppFooter',
    'Divider',
    'PageHeader',
    'PageContent',
    'Menu',
    'Link',
    'Text',
    'Table',
    'Pagination',
    'Select',
    'Radio',
    'ChatBubble',
    'FileInput',
    'SSEChat',
    'DataTable',
    'Range',
    # then `AnyComponent` itself
    'AnyUI',
)

from fai_backend.new_chat.models import ClientChatState
from fai_backend.config import settings
from fai_backend.framework import events as e
from fai_backend.framework.table import DataTable


class UIComponent(BaseModel, extra='forbid'):
    type: str
    id: str | None = None
    class_name: str | None = Field(None, serialization_alias='class')
    components: list | None = Field(None, serialization_alias='renderProps.components')


class Div(UIComponent):
    type: Literal['Div'] = 'Div'
    style: str | None = None


class Text(UIComponent):
    type: Literal['Text'] = 'Text'
    text: str
    element: Literal['p', 'span', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'] = 'span'
    state: Literal[
               'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = None

    icon_src: str | None = Field(None, serialization_alias='iconSrc')
    icon_state: Literal[
                    'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = Field(
        None, serialization_alias='iconState')
    badge: str | int | None = None
    badge_state: Literal[
                     'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = Field(
        None, serialization_alias='badgeState')


class Heading(Text):
    type: Literal['Heading'] = 'Heading'
    level: Literal[1, 2, 3, 4] = 2
    element: None = Field(None, exclude=True)


class Button(UIComponent):
    type: Literal['Button'] = 'Button'
    label: str
    state: Literal[
               'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = None
    html_type: Literal['submit', 'button'] = 'button'
    block: bool | None = None
    variant: Literal['outline', 'ghost'] | None = None
    on_click: e.AnyEvent | None = Field(None, serialization_alias='onClick')

    icon_src: str | None = Field(None, serialization_alias='iconSrc')
    icon_state: Literal[
                    'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = Field(
        None, serialization_alias='iconState')
    badge: str | int | None = None
    badge_state: Literal[
                     'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = Field(
        None, serialization_alias='badgeState')
    size: Literal['xs', 'sm', 'md', 'lg'] | None = None


class Form(UIComponent):
    type: Literal['Form'] = 'Form'
    submit_url: str = Field(None, serialization_alias='action')
    method: Literal['POST', 'GET', 'PATCH'] = 'POST'
    submit_text: str | None = None
    submit_as: Literal['json', 'form'] | None = Field('json', serialization_alias='submitAs')


class InputField(UIComponent):
    type: Literal['InputField'] = 'InputField'
    name: str
    title: str | None = None
    label: str | None = None
    placeholder: str | None = None
    required: bool | None = None
    html_type: Literal['text', 'password', 'hidden', 'number', 'email', 'tel', 'file'] = 'text'
    initial: str | None = Field(None, serialization_alias='value')
    hidden: bool = None
    disabled: bool | None = None
    autocomplete: str | None = None
    readonly: bool | None = None
    input_state: Literal[
                     'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = None
    value: str | None = None
    size: Literal['xs', 'sm', 'md', 'lg'] | None = None


class FileInput(InputField):
    type: Literal['FileInput'] = 'FileInput'
    name: str
    title: str | None = None
    required: bool | None = None
    accept: str | None = None
    file_size_limit: int | None = Field(None, serialization_alias='fileSizeLimit')
    multiple: bool | None = None

    # Remove the following fields from the base class
    placeholder: None = None
    initial: None = None
    hidden: None = None
    autocomplete: None = None
    readonly: None = None
    input_state: None = None
    value: None = None
    html_type: None = None


class Textarea(UIComponent):
    type: Literal['Textarea'] = 'Textarea'
    name: str
    title: str | None = None
    label: str | None = None
    placeholder: str | None = None
    required: bool | None = None
    initial: str | None = Field(None, serialization_alias='value')
    variant: Literal['ghost', 'bordered'] | None = None
    hidden: bool = None
    class_name: str | None = Field(None, serialization_alias='class')
    autocomplete: str | None = None
    readonly: bool | None = None
    rows: int | None = None
    state: Literal[
               'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success'] | None = None
    size: Literal['xs', 'sm', 'md', 'lg'] | None = None
    value: str | None = None


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
    sub_menu: bool | None = Field(None, serialization_alias='subMenu')
    size: Literal['xs', 'sm', 'md', 'lg'] | None = None
    components: 'list[AnyUI] | None' = Field(None, serialization_alias='renderProps.components')
    icon_src: str | None = Field(None, serialization_alias='iconSrc')
    icon_state: Literal[
                    'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = Field(
        None, serialization_alias='iconState')


class Link(Text):
    type: Literal['Link'] = 'Link'
    url: str | None = Field(None, serialization_alias='href')
    element: None = Field(None, exclude=True)
    state: Literal['primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success'] | None = None
    underline: Literal['on-hover', 'always', 'never'] | bool | None = None
    active: bool | str = False
    disabled: bool | None = None


class AppContent(UIComponent):
    type: Literal['AppContent'] = 'AppContent'


class PageHeader(UIComponent):
    type: Literal['PageHeader'] = 'PageHeader'


class PageContent(UIComponent):
    type: Literal['PageContent'] = 'PageContent'


class AppFooter(UIComponent):
    type: Literal['AppFooter'] = 'AppFooter'


class FireEvent(UIComponent):
    type: Literal['FireEvent'] = 'FireEvent'
    event: 'e.AnyEvent'


class Table(UIComponent):
    type: Literal['Table'] = 'Table'
    data: list[dict]
    columns: list[dict]
    row_class: str | None = Field(None, serialization_alias='rowClass')
    cell_class: str | None = Field(None, serialization_alias='cellClass')
    header_class: str | None = Field(None, serialization_alias='headerClass')


class Pagination(UIComponent):
    type: Literal['Pagination'] = 'Pagination'
    current: int
    total: int
    limit: int = 5
    query_var: str = 'page'


class Select(BaseModel):
    type: Literal['Select'] = 'Select'
    id: str | None = None
    class_name: str | None = Field(None, serialization_alias='class')
    name: str
    title: str | None = None
    label: str | None = None
    placeholder: str | None = None
    required: bool | None = None

    initial: str | None = Field(None, serialization_alias='value')
    hidden: bool = None

    readonly: bool | None = None
    input_state: Literal[
                     'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = None
    value: str | None = None
    options: list[tuple[str, str | None]] | None = None
    size: Literal['xs', 'sm', 'md', 'lg'] | None = None


class Radio(UIComponent):
    type: Literal['Radio'] = 'Radio'
    name: str
    title: str | None = None
    required: bool | None = None
    options: list[tuple[str, str | None]] | None = None


class ChatBubble(UIComponent):
    type: Literal['ChatBubble'] = 'ChatBubble'
    image_src: str | None = Field(None, serialization_alias='imageSrc')
    user: str | None = None
    content: str
    time: str | None = None
    is_self: bool | None = Field(None, serialization_alias='isSelf')
    footer: 'list[AnyUI] | None' = Field(None, serialization_alias='slot.footer')


class Divider(UIComponent):
    type: Literal['Divider'] = 'Divider'
    text: str | None = None
    state: Literal['primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = None


class SSEDocument(BaseModel):
    id: str
    name: str


class Assistant(BaseModel):
    id: str
    name: str
    project: str
    description: str
    sampleQuestions: list[str]
    maxTokens: int
    allowInlineFiles: bool


class SSEChat(UIComponent):
    type: Literal['SSEChat'] = 'SSEChat'
    assistants: list[Assistant] = []
    chat_initial_state: ClientChatState | None = Field(None, serialization_alias='initialState')


class Range(UIComponent):
    type: Literal['Range'] = 'Range'
    name: str
    title: str | None = None
    label: str | None = None
    required: bool | None = None
    hidden: bool = None
    disabled: bool | None = None
    readonly: bool | None = None
    input_state: Literal[
                     'primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success', 'neutral'] | None = None
    value: int | float | None = None
    size: Literal['xs', 'sm', 'md', 'lg'] | None = None
    min: int | float | None = None
    max: int | float | None = None
    step: int | float | None = None


AnyUI = Annotated[
    (Div | Form | InputField | Button | FireEvent | Heading |
     AppShell | AppDrawer | AppContent | AppFooter | Divider | PageHeader |
     PageContent | Menu | Link | Textarea | Text | Table | Pagination | Select | Radio |
     ChatBubble | FileInput | SSEChat | DataTable | Range),
    Field(discriminator='type')
]
