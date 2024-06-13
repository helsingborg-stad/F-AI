from fai_backend.framework import components as c
from fai_backend.icons import icons
from fai_backend.phrase import phrase as _
from fai_backend.qaf.schema import QuestionFilterParams
from fai_backend.qaf.service import QAFService
from fai_backend.schema import ProjectUser
from fai_backend.views import permission_required


async def build_qa_menu_items(
        project_user: ProjectUser,
        qaf_service: QAFService
) -> list[tuple[str, str, str]]:
    status_tabs = ['open', 'in-progress', 'rejected', 'approved']

    async def get_count_by_review_status(status: str):
        return len(await qaf_service.list_submitted_questions(
            project_user=project_user,
            query_params=QuestionFilterParams(review_status=status),
        ))

    return [
        *[
            (
                f'{status.capitalize()}',
                f'/questions?review_status={status}',
                await get_count_by_review_status(status) or '0',

            )
            for status in status_tabs
        ],
    ]


@permission_required(['can_review_answers'])
def qa_menu(
        items: list[tuple[str, str, str]] = None,
) -> list:
    return [
        c.Menu(
            title=_('questions', 'Questions'),
            id='questions-menu',
            variant='vertical',
            sub_menu=True,
            icon_src=icons['messages_square'],
            components=[
                c.Link(
                    text=_('show_all', 'Visa alla'),
                    url='/questions',
                    active='/questions*'
                ),
                c.Menu(
                    title=_('status', 'Status'),
                    components=[
                        *[c.Link(
                            text=text,
                            url=url,
                            active=url,
                            badge=badge,
                        ) for text, url, badge in (items or [])]
                    ]
                ),
                c.Link(
                    text=_('Add new question'),
                    url='/questions/create',
                    active='/questions/create',
                    icon_src=icons['square_pen'],
                ),
            ],
        ),
    ]
