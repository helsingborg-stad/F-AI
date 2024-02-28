from typing import TypeVar, Union, List, Sequence, Dict
from typing_extensions import Literal

T = TypeVar('T')
LogicalOperator = Union[Literal["$and"], Literal["$or"]]
LiteralValue = Union[str, int, float, bool]
WhereOperator = Union[
    Literal["$gt"],
    Literal["$gte"],
    Literal["$lt"],
    Literal["$lte"],
    Literal["$ne"],
    Literal["$eq"],
]
InclusionExclusionOperator = Union[Literal["$in"], Literal["$nin"]]
OperatorExpression = Union[
    Dict[Union[WhereOperator, LogicalOperator], LiteralValue],
    Dict[InclusionExclusionOperator, List[LiteralValue]],
]
OneOrMany = Union[T, List[T]]
Vector = Union[Sequence[float], Sequence[int]]
Embedding = Vector
Include = List[
    Union[
        Literal["documents"],
        Literal["embeddings"],
        Literal["metadatas"],
        Literal["distances"],
        Literal["uris"],
        Literal["data"],
    ]
]
Document = str
Where = Dict[
    Union[str, LogicalOperator], Union[LiteralValue, OperatorExpression, List["Where"]]
]