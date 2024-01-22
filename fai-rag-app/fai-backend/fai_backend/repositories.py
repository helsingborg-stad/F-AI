import time
from typing import Protocol

from beanie import Document, Indexed
from pydantic import EmailStr, Field

from fai_backend.conversations.models import ConversationModel
from fai_backend.projects.schema import Project
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
        projects = await self.list()
        user_projects = [
            project
            for project in projects
            if email in [member.email for member in project.members]
        ]

        def user_projects_to_user_roles(
                project_list: list[Project],
        ) -> list[ProjectUserRole]:
            return [
                ProjectUserRole(
                    project_id=str(project.id),
                    role=next(
                        member.role
                        for member in project.members
                        if member.email == email
                    ),
                    permissions=(project.model_dump())['roles'][
                        next(
                            member.role
                            for member in project.members
                            if member.email == email
                        )
                    ]['permissions'],
                )
                for project in project_list
            ]

        return (
            User(
                email=email,
                projects=user_projects_to_user_roles(user_projects),
            )
            if len(user_projects) > 0
            else None
        )


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


class ConversationDocument(ConversationModel, Document):
    class Settings:
        name = 'conversations'


class ConversationRepository(IAsyncRepo[ConversationDocument]):
    pass


repo_factory.register_builder(
    {
        ProjectRepository: lambda: create_repo_from_env(ProjectModel),
        UserRepository: lambda: UserRepoImp([create_repo_from_env(ProjectModel)]),
        PinCodeRepository: lambda: create_repo_from_env(PinCodeModel),
        ConversationRepository: lambda: create_repo_from_env(ConversationDocument),
    }
)

projects_repo = repo_factory.create(ProjectRepository)
users_repo = repo_factory.create(UserRepository)
pins_repo = repo_factory.create(PinCodeRepository)
conversation_repo = repo_factory.create(ConversationRepository)
