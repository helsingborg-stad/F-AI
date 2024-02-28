from typing import Callable, TypeVar, Dict, Type

from fai_backend.config import settings

from fai_backend.vector.chromadb import ChromaDBVector
from fai_backend.vector.interface import IVector
from fai_backend.vector.memory import InMemoryVectorDB

T = TypeVar('T', bound=IVector)  # Ensure that all registered types adhere to the IVector interface


class VectorDBFactory:
    _builders: Dict[str, Callable[..., T]] = {}

    @classmethod
    def register(cls, db_type: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
        """Decorator to register a new builder with the factory."""

        def decorator(builder: Callable[..., T]) -> Callable[..., T]:
            if db_type in cls._builders:
                raise KeyError(f"A builder for '{db_type}' is already registered.")
            cls._builders[db_type] = builder
            return builder

        return decorator

    @classmethod
    def create(cls, db_type: str, **kwargs) -> T:
        """Instantiate a new object of the given type."""
        if db_type not in cls._builders:
            raise KeyError(f"No builder registered for type {db_type}")
        return cls._builders[db_type](**kwargs)

    @classmethod
    def list_types(cls) -> Dict[str, Callable[..., T]]:
        """Return a list of the registered types."""
        return cls._builders


@VectorDBFactory.register('chromadb')
def create_chromadb_vector() -> IVector:
    return ChromaDBVector(db_directory=settings.APP_VECTOR_DB_PATH)


@VectorDBFactory.register('memory')
def create_in_memory_vector() -> IVector:
    return InMemoryVectorDB()


vector_db = VectorDBFactory.create(settings.APP_VECTOR_DB)
