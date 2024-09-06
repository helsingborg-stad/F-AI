from fai_backend.projects.schema import (
    Project,
    ProjectCreateRequest,
    ProjectUpdateRequest,
)
from fai_backend.repositories import ProjectModel, ProjectRepository


class ProjectService:
    repo: ProjectRepository

    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    async def create_project(self, project: ProjectCreateRequest) -> Project | None:
        return await self.repo.create(ProjectModel.model_validate(project.model_dump()))

    async def read_projects(self, skip: int = 0, limit: int = 100):
        return await self.repo.list()

    async def read_project(self, project_id: str):
        return await self.repo.get(project_id)

    async def update_project(self, project_id: str, project: ProjectUpdateRequest):
        updated_fields = self._extract_updated_fields(project)
        return await self.repo.update(project_id, updated_fields)

    async def delete_project(self, project_id: str):
        return await self.repo.delete(project_id)

    @staticmethod
    def _extract_updated_fields(project: ProjectUpdateRequest) -> dict:
        ignore_keys = ['id', 'timestamp']
        model_dump = project.model_dump()
        return {
            key: model_dump[key] for key in model_dump.keys() if key not in ignore_keys}
