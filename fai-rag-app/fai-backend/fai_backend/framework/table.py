import enum
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, Field

from fai_backend.framework.display import DisplayField
from fai_backend.framework.events import GoToEvent

T = TypeVar('T')


class ColumnFilter(str, enum.Enum):
    multi_select = 'multi-select'
    search = 'search'


class DataColumn(DisplayField):
    type: Literal['DisplayColumn'] = 'DisplayColumn'
    width: int | None = None
    align: Literal['left', 'center', 'right'] | None = None
    sortable: bool | None = None
    sort_order: Literal['asc', 'desc'] | None = Field(None, serialization_alias='sortOrder')
    filter: ColumnFilter | bool | None = None
    filter_options: list[tuple[str, str]] | None = Field(None, serialization_alias='filterOptions')
    filter_initial_value: str | None = Field(None, serialization_alias='filterInitialValue')
    hide_from_search: bool | None = Field(None, serialization_alias='hideFromSearch')
    hidden: bool | None = None
    on_click: GoToEvent | None = Field(None, serialization_alias='onClick')


class DataTable(BaseModel, Generic[T]):
    type: Literal['DataTable'] = 'DataTable'
    data: list[T]
    columns: list[DataColumn]
    columnOrder: list[str] | None = None
    initialFilterValue: str | None = None
    include_view_action: bool = Field(True, serialization_alias='includeViewAction')
