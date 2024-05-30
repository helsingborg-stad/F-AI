from beanie import init_beanie
from fastapi import FastAPI
from fastapi.routing import APIRoute
from motor.motor_asyncio import AsyncIOMotorClient

from fai_backend.config import settings
from fai_backend.projects.schema import ProjectMember, ProjectRole
from fai_backend.repositories import ConversationDocument, PinCodeModel, ProjectModel, projects_repo
from fai_backend.assistant.models import AssistantTemplate, LLMStreamSettings, LLMStream, LLMStreamMessage


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'

    return None


async def setup_project():
    projects = await projects_repo.list()
    if not projects or len(projects) == 0:
        def create_permissions(value: bool):
            permissions = [
                'can_edit_project_users',
                'can_edit_project_roles',
                'can_edit_project_secrets',
                'can_ask_questions',
                'can_review_answers',
                'can_edit_questions_and_answers',
            ]
            return {
                x: y
                for x, y in zip(
                    permissions,
                    [value] * len(permissions),
                )
            }

        initial_project = await projects_repo.create(
            ProjectModel(
                name='Project',
                creator=settings.APP_ADMIN_EMAIL,
                assistants=[
                    AssistantTemplate(
                        name='Basic Assistant',
                        streams=[LLMStream(
                            name='ChatStream',
                            settings=LLMStreamSettings(model='gpt-4o'),
                            messages=[LLMStreamMessage(
                                role='system',
                                content="You are a helpful AI assistant that helps people with answering questions "
                                        "related to municipality and Helsingborg City. The questions are going to be "
                                        "asked in Swedish. Your response must always be in Swedish."
                            )]
                        )],
                    ),
                    AssistantTemplate(
                        name='Planning Assistant',
                        files_collection_id='please upload files in the Assistant UI',
                        streams=[
                            LLMStream(
                                name='ScoringStream',
                                settings=LLMStreamSettings(
                                    model='gpt-3.5-turbo',
                                    functions=[{
                                        "name": "score_document",
                                        "description": "Scores the previous document according to the user query\n\n  "
                                                       "  Parameters\n    ----------\n    score\n        A number "
                                                       "from 0-100 scoring how well does the document matches the "
                                                       "query. The higher the score, the better match for the query\n "
                                                       "   ",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {
                                                "score": {
                                                    "type": "number",
                                                }
                                            },
                                            "required": ["score"],
                                        }
                                    }],
                                    function_call={"name": "score_document"}
                                )
                            ),
                            LLMStream(
                                name='ChatStream',
                                settings=LLMStreamSettings(
                                    model='gpt-4o'
                                ),
                                messages=[
                                    LLMStreamMessage(
                                        role='system',
                                        content="You are a helpful AI assistant that helps people with answering "
                                                "questions about planning permission.<br> If you can't find the "
                                                "answer in the search result below, just say (in Swedish) \"Tyvärr "
                                                "kan jag inte svara på det.\" Don't try to make up an answer.<br> If "
                                                "the question is not related to the context, politely respond that "
                                                "you are tuned to only answer questions that are related to the "
                                                "context.<br> The questions are going to be asked in Swedish. Your "
                                                "response must always be in Swedish."
                                    ),
                                    LLMStreamMessage(
                                        role='user',
                                        content='{query}'
                                    ),
                                    LLMStreamMessage(
                                        role='user',
                                        content='Here are the results of the search:\n\n {results}'
                                    )
                                ]
                            )
                        ]
                    )
                ],
                members=[
                    ProjectMember(
                        email=settings.APP_ADMIN_EMAIL,
                        role='admin'
                    )
                ],
                roles={
                    'admin': ProjectRole(permissions=create_permissions(True)),
                    'manager': ProjectRole(permissions=create_permissions(False)),
                    'reviewer': ProjectRole(permissions=create_permissions(False)),
                    'tester': ProjectRole(permissions=create_permissions(False))
                },
                secrets={'openai_api_key': 'sk-123'},
                meta={}
            )
        )

        if initial_project:
            print('Initialized Initial Project')
        else:
            raise Exception('Failed to create initial project')


async def setup_db():
    client = AsyncIOMotorClient(settings.MONGO_DB_URI)
    await init_beanie(
        database=client[settings.MONGO_DB_NAME],
        document_models=[ProjectModel, PinCodeModel, ConversationDocument],
    )
