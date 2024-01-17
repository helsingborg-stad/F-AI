from typing import Annotated, Literal

from pydantic import BaseModel, Field

__all__ = (
    'Div',
    'Page',
    'Heading',
    'Button',
    'FireEvent',
    'Form',
    'InputField',
    # then `AnyComponent` itself
    'AnyUI',
)

from fai_backend.framework import events as e


class Div(BaseModel, extra='forbid'):
    type: Literal['Div'] = 'Div'
    class_name: str | None = Field(None, serialization_alias='class')
    components: 'list[AnyUI]'


class Heading(BaseModel, extra='forbid'):
    type: Literal['Heading'] = 'Heading'
    text: str
    class_name: str | None = Field(None, serialization_alias='class')


class Button(BaseModel, extra='forbid'):
    type: Literal['Button'] = 'Button'
    text: str
    html_type: Literal['submit', 'button'] = 'button'
    class_name: str | None = Field(None, serialization_alias='class')


class Form(BaseModel, extra='forbid'):
    submit_url: str = Field(None, serialization_alias='action')
    type: Literal['Form'] = 'Form'
    class_name: str | None = Field(None, serialization_alias='class')
    components: 'list[AnyUI]'
    method: Literal['POST', 'GET']
    submit_text: str | None = None


class InputField(BaseModel, extra='forbid'):
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


class Page(BaseModel, extra='forbid'):
    type: Literal['Page'] = 'Page'
    components: 'list[AnyUI]'


class FireEvent(BaseModel, extra='forbid'):
    type: Literal['FireEvent'] = 'FireEvent'
    event: 'e.AnyEvent'


AnyUI = Annotated[
    Div | Form | InputField | Button | FireEvent | Heading | Page,
    Field(discriminator='type')
]
