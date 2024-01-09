from fastui import AnyComponent, components as c
from fastui.events import GoToEvent


def page_template(
    *components: AnyComponent,
    title: str | None = None,
) -> list[AnyComponent]:
    return [
        c.PageTitle(text=f"FastUI Demo — {title}" if title else "FastUI Demo"),
        c.Navbar(
            title="Folkets Ai",
            title_event=GoToEvent(url="/"),
            links=[
                c.Link(
                    components=[c.Text(text="Conversations")],
                    on_click=GoToEvent(url="/conversations"),
                    active="startswith:/components",
                ),
                c.Link(
                    components=[c.Text(text="Logga ut")],
                    on_click=GoToEvent(url="/logout"),
                ),
            ],
        ),
        c.Page(
            components=[
                *((c.Heading(text=title),) if title else ()),
                *components,
            ],
        ),
        c.Footer(
            extra_text="Folkets AI",
            links=[],
        ),
    ]
