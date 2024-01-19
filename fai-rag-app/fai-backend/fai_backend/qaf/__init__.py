from fastapi import APIRouter, Depends

from fai_backend.dependencies import try_get_authenticated_user
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.schema import User
from phrase import phrase as _
from views import page_template

router = APIRouter(
    prefix='/api',
    tags=['QAF'],
    route_class=LoggingAPIRouter,
)


@router.get('/questions', response_model=list, response_model_exclude_none=True)
def questions_index_view(
        authenticated_user: User | None = Depends(try_get_authenticated_user),
) -> list:
    if not authenticated_user:
        return [c.FireEvent(event=e.GoToEvent(url='/login'))]

    return page_template(
        c.Heading(text='This is the questions page'),
        page_title=_('my_questions', 'My Questions'),
    )
