from abc import ABC
from pydantic import BaseModel, Field
from typing import Any, Dict, Literal, NotRequired, TypedDict


def try_neg_default(value: Any, key: str, model: BaseModel) -> bool:
    try:
        return model.__fields__[key].get_default() != value
    except Exception:
        return True


class BaseSerialized(TypedDict):
    fai: int
    id: list[str]
    name: NotRequired[str]
    graph: NotRequired[Dict[str, Any]]


class SerializedConstructor(BaseSerialized):
    type: Literal['constructor']
    kwargs: Dict[str, Any]


class Serializable(BaseModel, ABC):
    @classmethod
    def is_fai_serializable(cls) -> bool:
        return False

    @classmethod
    def get_fai_namespace(cls) -> list[str]:
        return cls.__module__.split('.')

    @classmethod
    def fai_id(cls) -> list[str]:
        return [*cls.get_fai_namespace(), cls.__name__]

    class Config:
        extra = 'ignore'

    def __repr_args__(self) -> Any:
        return [(k, v) for k, v in super().__repr_args__()
                if (k not in self.__fields__ or try_neg_default(v, k, self))]

    def to_json(self) -> SerializedConstructor | str:
        if not self.is_fai_serializable():
            return "Not serializable"

        fai_kwargs = {
            k: getattr(self, k, v) for k, v in self if not (self.__exclude_fields__ or {}).get(k, False)}
        return {
            'fai': 1,
            'type': 'constructor',
            'id': self.fai_id(),
            'kwargs': fai_kwargs}


class Document(Serializable):
    page_content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    type: Literal['Document'] = 'Document'

    def __init__(self, page_content: str, **kwargs: Any) -> None:
        super().__init__(page_content=page_content, **kwargs)

    @classmethod
    def is_fai_serializable(cls) -> bool:
        return True

    @classmethod
    def get_fai_namespace(cls) -> list[str]:
        return ['fai', 'schema', 'document']
