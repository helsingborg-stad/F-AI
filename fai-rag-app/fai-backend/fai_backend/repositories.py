import time
from typing import Protocol

from beanie import Document, Indexed
from pydantic import EmailStr, Field

from fai_backend.assistant.models import AssistantChatHistoryModel, StoredQuestionModel
from fai_backend.auth.security import try_match_email
from fai_backend.collection.models import CollectionMetadataModel
from fai_backend.conversations.models import Conversation
from fai_backend.projects.schema import Project, ProjectMember
from fai_backend.repository.composite import CompositeRepo
from fai_backend.repository.factory import create_repo_from_env
from fai_backend.repository.factory import factory as repo_factory
from fai_backend.repository.interface import IAsyncRepo
from fai_backend.schema import ProjectUserRole, User


class ProjectModel(Document, Project):
    class Settings:
        name = 'projects'
        use_state_management = True


class ProjectRepository(IAsyncRepo[ProjectModel]):
    pass


class UserRepository(Protocol):
    async def get_user_by_email(self, email: str) -> User:
        pass

    async def list_users(self) -> list[User]:
        pass


class UserRepoImp(UserRepository, CompositeRepo[ProjectModel]):
    async def list_users(self) -> list[User]:
        projects = await self.list()
        return [
            User.model_validate(member)
            for project in projects
            for member in project.members
        ]

    async def get_user_by_email(self, email: str) -> User | None:

        def filter_user_projects(project_list: list[Project], _email: str) -> list[Project]:
            # TODO: fix hack handling wildcard
            exact_match = [project for project in project_list if
                           _email in [member.email for member in project.members if member.is_pattern is False]]

            if exact_match:
                return exact_match

            pattern_matches = [[m for m in project.members if m.is_pattern] for project in project_list]

            for pattern_entry in pattern_matches:
                pattern = next(p.email for p in pattern_entry)

                if try_match_email(_email, pattern):
                    new_project = project_list[0].model_copy(deep=True)

                    new_project.members = [
                        ProjectMember(email=_email, is_pattern=False, role=member.role) if member.is_pattern else member
                        for member in new_project.members
                    ]

                    return [new_project]
                else:
                    return []

        def user_projects_to_user_roles(project_list: list[Project]) -> list[ProjectUserRole]:
            return [
                ProjectUserRole(
                    project_id=str(project.id),
                    role=next(member.role for member in project.members if member.email == email),
                    permissions=(project.model_dump())['roles'][
                        next(member.role for member in project.members if member.email == email)
                    ]['permissions'],
                ) for project in project_list
            ]

        user_projects = filter_user_projects(await self.list(), email)

        return User(
            email=email,
            projects=user_projects_to_user_roles(user_projects)
        ) if len(user_projects) > 0 else None


class PinCodeModel(Document):
    email: Indexed(EmailStr)
    hashed_pin: str
    expiry: float = Field(
        default_factory=lambda: time.time() + 900  # 15 minutes expiry
    )

    class Settings:
        name = 'pin'


class PinCodeRepository(IAsyncRepo[PinCodeModel]):
    pass


class ConversationDocument(Document, Conversation):
    class Settings:
        name = 'conversations'
        use_state_management = True


class ConversationRepository(IAsyncRepo[Conversation]):
    pass


class ChatHistoryRepository(IAsyncRepo[AssistantChatHistoryModel]):
    pass


class CollectionMetadataRepository(IAsyncRepo[CollectionMetadataModel]):
    pass


class StoredQuestionsRepository(IAsyncRepo[StoredQuestionModel]):
    pass


repo_factory.register_builder(
    {
        ProjectRepository: lambda: create_repo_from_env(ProjectModel, ProjectModel),
        UserRepository: lambda: UserRepoImp([create_repo_from_env(ProjectModel, ProjectModel)]),
        PinCodeRepository: lambda: create_repo_from_env(PinCodeModel, PinCodeModel),
        ConversationRepository: lambda: create_repo_from_env(Conversation, ConversationDocument),
        ChatHistoryRepository: lambda: create_repo_from_env(AssistantChatHistoryModel, AssistantChatHistoryModel),
        CollectionMetadataRepository: lambda: create_repo_from_env(CollectionMetadataModel, CollectionMetadataModel),
        StoredQuestionsRepository: lambda: create_repo_from_env(StoredQuestionModel, StoredQuestionModel),
    }
)

projects_repo = repo_factory.create(ProjectRepository)
users_repo = repo_factory.create(UserRepository)
pins_repo = repo_factory.create(PinCodeRepository)
conversation_repo = repo_factory.create(ConversationRepository)
chat_history_repo = repo_factory.create(ChatHistoryRepository)
collection_metadata_repo = repo_factory.create(CollectionMetadataRepository)
stored_questions_repo = repo_factory.create(StoredQuestionsRepository)
