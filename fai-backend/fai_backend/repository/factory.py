from collections.abc import Callable
from typing import TypeVar

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
            builder_info: dict[type[T], Callable[[], T]] | type[T] | Callable[[], T],
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
T = TypeVar('T')
T_DB = TypeVar('T_DB')


def create_repo_from_env(model_type: type[T], db_type: type[T_DB], app_db: str = settings.APP_DB) -> IAsyncRepo[T]:
    def create_repo_factory_map() -> dict[str, Callable[[], IAsyncRepo[T]]]:
        return {
            'mongodb': lambda: MongoDBRepo[T, T_DB](model_type, db_type),
            'memory': lambda: InMemoryRepo[T](),
        }

    repo_factory_map = create_repo_factory_map()
    return repo_factory_map[app_db]()
