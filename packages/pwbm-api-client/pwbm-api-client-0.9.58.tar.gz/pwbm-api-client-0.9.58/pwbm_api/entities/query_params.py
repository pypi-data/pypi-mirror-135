from enum import Enum
from typing import Optional, List
from uuid import UUID

from pydantic import StrictStr, StrictInt, StrictBool

from .base import BaseModel
from .date_range import DateRange
from .tag import TagEntity


class SortType(str, Enum):
    ascending = 'asc'
    descending = 'desc'


class LocationGranularity(str, Enum):
    national = 'national'
    state = 'state'
    county = 'county'


class SeriesSortBy(str, Enum):
    NAME = 'name'
    UNIT_OF_MEASUREMENT = 'uom'
    FREQUENCY = 'frequency'
    SOURCE = 'source'
    START_DATE = 'start_date'
    END_DATE = 'end_date'


class SeriesSortByDB(str, Enum):
    NAME = 'name'
    UNIT_OF_MEASUREMENT = 'uom'
    SOURCE = 'source'
    START_DATE = 'start_date'
    END_DATE = 'end_date'
    CREATED = 'row_ver'


class TablesSortBy(str, Enum):
    NAME = 'name'
    SOURCE = 'source'


class TablesSortByDB(str, Enum):
    NAME = 'name'
    SOURCE = 'source'
    CREATED = 'row_ver'


class BaseSorting(BaseModel):
    client_side: bool = False
    sort: Optional[SortType]


class SeriesDBSorting(BaseSorting):
    sort_by: Optional[SeriesSortByDB]


class SeriesIndexSorting(BaseSorting):
    sort_by: Optional[SeriesSortBy]


class TablesDBSorting(BaseSorting):
    sort_by: Optional[TablesSortByDB]


class TablesIndexSorting(BaseSorting):
    sort_by: Optional[TablesSortBy]


class SeriesQueryClientEntity(BaseModel):
    sources: Optional[List[StrictStr]]
    frequencies: Optional[List[StrictStr]]
    uoms: Optional[List[StrictStr]]
    relates_to_table: Optional[StrictBool]
    date_range: Optional[DateRange]
    tags: Optional[List[TagEntity]]


class SeriesQueryEntity(BaseModel):
    search_text: Optional[List[StrictStr]]
    sources: Optional[List[StrictStr]]
    frequencies: Optional[List[StrictStr]]
    uoms: Optional[List[StrictStr]]
    relates_to_table: Optional[StrictBool]
    date_range: Optional[DateRange]
    tags: Optional[List[TagEntity]]


class TablesQueryClientEntity(BaseModel):
    sources: Optional[List[StrictStr]]


class TableQueryEntity(BaseModel):
    search_text: Optional[List[StrictStr]]
    sources: Optional[List[StrictStr]]


class SearchByNeumQuery(BaseModel):
    neum: Optional[StrictStr] = ''


class SearchSeriesByMetricQuery(BaseModel):
    metric_id: UUID
    granularity: Optional[LocationGranularity]
    page_size: Optional[StrictInt]
    page_num: Optional[StrictInt]
