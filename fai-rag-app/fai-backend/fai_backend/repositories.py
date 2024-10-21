import time
from typing import Protocol

from beanie import Document, Indexed
from pydantic import EmailStr, Field

from fai_backend.assistant.models import AssistantChatHistoryModel, StoredQuestionModel
from fai_backend.auth.security import is_mail_pattern, try_match_email
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

        def extract_member_emails(member_list: list[ProjectMember]) -> list[str]:
            return [m.email for m in member_list]

        def find_exact_matches(project_list: list[Project]) -> list[Project]:
            return [p for p in project_list if
                    email in extract_member_emails(p.members) and not is_mail_pattern(email)]

        def filter_user_projects(project_list: list[Project]) -> list[Project]:
            exact_match_projects = find_exact_matches(project_list)

            if exact_match_projects:
                return exact_match_projects

            for proj in project_list:
                pattern = next(pattern for pattern in extract_member_emails(proj.members) if is_mail_pattern(pattern))

                if try_match_email(email, pattern):
                    new_project = proj.model_copy(deep=True)
                    new_project.members.append(
                        ProjectMember(email=email,
                                      role=next(m.role for m in new_project.members if m.email == pattern)))
                    return [new_project]

            return []

        def user_projects_to_user_roles(project_list: list[Project]) -> list[ProjectUserRole]:
            return [
                ProjectUserRole(
                    project_id=str(project_.id),
                    role=next(member.role for member in project_.members if member.email == email),
                    permissions=(project_.model_dump())['roles'][
                        next(member.role for member in project_.members if member.email == email)
                    ]['permissions'],
                ) for project_ in project_list
            ]

        user_projects = filter_user_projects(await self.list())

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
