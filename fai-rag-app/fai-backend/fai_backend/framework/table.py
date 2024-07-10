import enum
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, Field

from fai_backend.framework.display import DisplayField

T = TypeVar('T')


class ColumnFilterControl(str, enum.Enum):
    select = 'select'
    multi_select = 'multi-select'
    search = 'search'


class DataColumn(DisplayField):
    type: Literal['DisplayColumn'] = 'DisplayColumn'
    width: int | None = None
    align: Literal['left', 'center', 'right'] | None = None
    sortable: bool | None = None
    sort_order: Literal['asc', 'desc'] | None = Field(None, serialization_alias='sortOrder')
    filter: ColumnFilterControl | bool | None = None
    filter_options: list[tuple[str, str]] | None = Field(None, serialization_alias='filterOptions')
    filter_initial_value: str | None = Field(None, serialization_alias='filterInitialValue')
    hide_from_search: bool | None = Field(None, serialization_alias='hideFromSearch')
    hidden: bool | None = None


class DataTable(BaseModel, Generic[T]):
    type: Literal['DataTable'] = 'DataTable'
    data: list[T]
    columns: list[DataColumn]
    columnOrder: list[str] | None = None
    initialFilterValue: str | None = None
