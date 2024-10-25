from typing import Any, Callable

from fastapi import APIRouter, Depends

from fai_backend.dependencies import get_page_template_for_logged_in_users
from fai_backend.feedback.models import FeedbackEntry
from fai_backend.feedback.service import FeedbackService, get_feedback_service
from fai_backend.feedback.views import feedback_submit_view, feedback_view
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter

router = APIRouter(
    prefix='/api',
    tags=['Feedback'],
    route_class=LoggingAPIRouter,
)


@router.get('/feedback', response_model=list, response_model_exclude_none=True)
def feedback_index_view(
        view: Callable[[list[Any], str | None], list[Any]] = Depends(get_page_template_for_logged_in_users)) -> list:

    return feedback_view(view, '/api/feedback/create')


@router.post('/feedback/create', response_model=list, response_model_exclude_none=True)
async def create_feedback(data: FeedbackEntry,
                    feedback_service: FeedbackService = Depends(get_feedback_service),
                    view: Callable[[list[Any], str | None], list[Any]] = Depends(
                        get_page_template_for_logged_in_users)) -> list:

    await feedback_service.send(data)

    return feedback_submit_view(view)
