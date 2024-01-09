from collections.abc import Callable
from typing import TypeVar, Union

from fai_backend.config import settings
from fai_backend.repository.interface import IAsyncRepo
from fai_backend.repository.memory import InMemoryRepo
from fai_backend.repository.mongodb import MongoDBRepo

T = TypeVar('T')


class RepositoryFactory:
    def __init__(self):
        self._builders: dict[type[T], Callable[[], T]] = {}

    def register_builder(
            self,
            builder_info: Union[dict[type[T], Callable[[], T]], type[T], Callable[[], T]],
    ):
        if isinstance(builder_info, dict):
            for type_, builder in builder_info.items():
                self._builders[type_] = builder
        else:
            type_, builder = builder_info
            self._builders[type_] = builder

    def create(self, type_: type[T]) -> T:
        builder = self._builders.get(type_)
        if not builder:
            raise ValueError(f'No builder registered for type {type_}')
        return builder()


factory = RepositoryFactory()
M = TypeVar('M')


def create_repo_from_env(model: type[M], app_db: str = settings.APP_DB) -> IAsyncRepo[M]:
    def create_repo_factory_map(
            db_model: type[M],
    ) -> dict[str, Callable[[], IAsyncRepo[M]]]:
        return {
            'mongodb': lambda: MongoDBRepo[M](db_model),
            'memory': lambda: InMemoryRepo[M](),
        }

    repo_factory_map = create_repo_factory_map(model)
    return repo_factory_map[app_db]()
