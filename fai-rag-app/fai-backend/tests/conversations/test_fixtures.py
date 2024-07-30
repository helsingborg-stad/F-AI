import pytest
import pytest_asyncio
from beanie import init_beanie
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from fai_backend.conversations.models import Conversation
from fai_backend.conversations.schema import CreateConversationRequest, CreateMessageRequest
from fai_backend.conversations.service import ConversationService
from fai_backend.repositories import ConversationDocument, ConversationRepository
from fai_backend.repository.mongodb import MongoDBRepo
from fai_backend.schema import ProjectUser

TEST_USER_EMAIL = "user@example.com"
DARK_MATTER_QUESTION = "What is dark matter?"
DARK_MATTER_ANSWER = ("Dark matter is a form of matter thought to account for approximately 85% of the matter in the "
                      "universe.")
MEANING_OF_LIFE_QUESTION = "What is the meaning of life?"


@pytest_asyncio.fixture
async def conversation_repo() -> ConversationRepository:
    client = AsyncIOMotorClient()
    await init_beanie(database=client['test-db'], document_models=[ConversationDocument])
    yield MongoDBRepo[Conversation, ConversationDocument](Conversation, ConversationDocument)
    await ConversationDocument.get_motor_collection().drop()


@pytest_asyncio.fixture
async def conversation_service(conversation_repo):
    return ConversationService(conversation_repo=conversation_repo)


@pytest.fixture
def project_admin_user():
    return ProjectUser(
        email=TEST_USER_EMAIL,
        permissions={"can_ask_questions": True},
        project_id="123",
        role="admin"
    )


@pytest.fixture
def create_dark_matter_question(project_admin_user):
    question = DARK_MATTER_QUESTION
    question_meta = {
        "errand_id": "sk-123",
        "subject": "Physics"
    }
    question_tag = ["physics"]

    return CreateConversationRequest(
        id=ObjectId(),
        type='question',
        messages=[
            CreateMessageRequest(
                user='user',
                created_by=project_admin_user.email,
                content=question,
                type='question'
            )
        ],
        metadata=question_meta,
        tags=question_tag
    )


@pytest.fixture
def create_meaning_of_life_question(project_admin_user):
    question = MEANING_OF_LIFE_QUESTION
    question_meta = {
        "errand_id": "sk-456",
        "subject": "Philosophy"
    }
    question_tag = ["philosophy"]

    return CreateConversationRequest(
        type='question',
        messages=[
            CreateMessageRequest(
                user='user',
                created_by=project_admin_user.email,
                content=question,
                type='question'
            )
        ],
        metadata=question_meta,
        tags=question_tag
    )
