from beanie import init_beanie
from fastapi import FastAPI
from fastapi.routing import APIRoute
from motor.motor_asyncio import AsyncIOMotorClient

from fai_backend.config import settings
from fai_backend.projects.schema import ProjectMember, ProjectRole
from fai_backend.repositories import ConversationDocument, PinCodeModel, ProjectModel, projects_repo
from fai_backend.assistant.models import AssistantTemplate, LLMStreamSettings, LLMStreamDef, LLMStreamMessage


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
                        id='example',
                        name='Example Assistant',
                        streams=[LLMStreamDef(
                            name='ChatStream',
                            settings=LLMStreamSettings(model='gpt-4o'),
                            messages=[
                                LLMStreamMessage(
                                    role='system',
                                    content="You are a helpful AI assistant that helps people with answering "
                                            "questions related to municipality and Helsingborg City. The "
                                            "questions are going to be asked in Swedish. Your response must "
                                            "always be in Swedish."
                                ),
                                LLMStreamMessage(
                                    role='user',
                                    content="{query}"
                                )
                            ]
                        )],
                    ),
                    AssistantTemplate(
                        id='multi_example',
                        name='Multi-stream Example',
                        streams=[
                            LLMStreamDef(
                                name='First Stream',
                                settings=LLMStreamSettings(model='gpt-4o'),
                                messages=[
                                    LLMStreamMessage(
                                        role='system',
                                        content="Make this text sound more fancy and verbose."
                                    ),
                                    LLMStreamMessage(
                                        role='user',
                                        content="{query}"
                                    )
                                ]
                            ),
                            LLMStreamDef(
                                name='Second Stream',
                                settings=LLMStreamSettings(model='gpt-4o'),
                                messages=[
                                    LLMStreamMessage(
                                        role='system',
                                        content="Repeat back any text verbatim and count the number of words"
                                    ),
                                    LLMStreamMessage(
                                        role='user',
                                        content="{last_input}"
                                    )
                                ]
                            )
                        ]
                    ),
                    AssistantTemplate(
                        id='rag_example',
                        name='RAG (document) Example',
                        files_collection_id='Upload files in the Assistant Creation UI',
                        streams=[LLMStreamDef(
                            name='RagStream',
                            settings=LLMStreamSettings(model='gpt-4o'),
                            messages=[
                                LLMStreamMessage(
                                    role='system',
                                    content="Explain what this is and repeat back an excerpt of it."
                                ),
                                LLMStreamMessage(
                                    role='user',
                                    content="{rag_results}"
                                )
                            ]
                        )]
                    ),
                    AssistantTemplate(
                        id='planning',
                        name='Planning Assistant',
                        files_collection_id='Upload files in the Assistant Creation UI',
                        streams=[
                            LLMStreamDef(
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
                                        content='Here are the results of the search:\n\n {rag_results}'
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
