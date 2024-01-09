from fastapi import Depends
from fastui import AnyComponent, components as c
from fastui.events import GoToEvent, PageEvent
from pydantic import BaseModel

from fai_backend.conversations.dependencies import (
    list_conversations_request,
    create_conversation_request,
    get_conversation_request,
)
from fai_backend.conversations.schema import (
    ResponseConversation,
)
from fai_backend.views import page_template


def conversations_list_view(
    conversations: list[ResponseConversation] = Depends(list_conversations_request),
) -> list[AnyComponent]:
    def items():
        return (
            c.Paragraph(text="No conversations")
            if not conversations or len(conversations) == 0
            else c.Table(
                data=conversations,
                data_model=ResponseConversation,
                columns=[
                    c.display.DisplayLookup(
                        field="id",
                        on_click=GoToEvent(url="./{id}"),
                        table_width_percent=33,
                    ),
                ],
            )
        )

    return page_template(*[c.Heading(text="Conversations"), items()])


class CreateConversationMessageModel(BaseModel):
    user: str
    content: str


class CreateConversationModel(BaseModel):
    messages: tuple[CreateConversationMessageModel]


def conversations_create_view(
    # conversations: list[ResponseConversation] = Depends(list_conversations_request),
) -> list[AnyComponent]:
    return page_template(
        *[
            c.Heading(text="Create"),
            c.Button(
                text="Add message",
                on_click=PageEvent(name="server-load"),
            ),
            c.ServerLoad(
                path=".",
                load_trigger=PageEvent(name="server-load"),
                components=[c.Text(text="before")],
            ),
            c.ModelForm(
                model=CreateConversationModel,
                submit_url="/api/conversations/create",
                class_name="col-xs-12",
                footer=[c.Button(text="Login", html_type="submit")],
            ),
        ]
    )


def handle_create_conversation(
    conversation: ResponseConversation = Depends(create_conversation_request),
) -> list[AnyComponent]:
    return [c.FireEvent(event=GoToEvent(url=f"./{conversation.id}"))]


def conversation_view(
    conversation: ResponseConversation = Depends(get_conversation_request),
) -> list[AnyComponent]:
    return page_template(*[c.Heading(text=conversation.id)])
