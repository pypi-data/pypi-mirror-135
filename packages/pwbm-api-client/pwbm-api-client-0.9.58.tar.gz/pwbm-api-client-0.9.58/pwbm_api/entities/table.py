from typing import Optional, List
from uuid import UUID

from pydantic import root_validator, validator

from .base import BaseModel
from .series_tag import SeriesTagEntity
from .series_value import SeriesValueEntity
from .source import SourceEntity


class TableEntity(BaseModel):
    id: UUID
    name: str


class LineAttributes(BaseModel):
    row_id: UUID
    number: int
    indent: int
    label: Optional[str]
    has_descendants: Optional[bool]


class DataItemInfo(BaseModel):
    id: Optional[UUID]
    name: Optional[str]
    priority: Optional[int]
    tables: Optional[List[TableEntity]]
    description: Optional[str]
    source: Optional[SourceEntity]
    periodicity: Optional[List[str]]
    data_type: Optional[str]
    date_range: str = '--'
    tags: Optional[List[SeriesTagEntity]]
    neums: Optional[List[str]]
    line_attributes: Optional[LineAttributes]
    data_items: Optional[List[SeriesValueEntity]]
    descendants: Optional[List['DataItemInfo']]

    @root_validator(pre=True)
    def prepare(cls, values):
        if 'info' in values:
            if info := values.pop('info'):
                values.update(info)
        return values

    @validator('source', pre=True)
    def prepare_source(cls, source):
        if isinstance(source, str):
            source = {'agency': source}
        return source


DataItemInfo.update_forward_refs()
