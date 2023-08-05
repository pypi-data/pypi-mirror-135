from typing import List, Optional
from uuid import UUID

from pydantic import root_validator, validator

from pwbm_api.entities import (
    BaseModel,
    SeriesTagEntity,
    SourceEntity,
    SeriesValueEntity,
    TableEntity
)
from pwbm_api.query import SeriesQuery


class Series(BaseModel):
    query = SeriesQuery

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
    data_items: Optional[List[SeriesValueEntity]]

    @validator('source', pre=True)
    def prepare_source(cls, source):
        if isinstance(source, str):
            source = {'agency': source}
        return source


class SeriesItems(BaseModel):
    __root__: List[Series]

    @root_validator(pre=True)
    def prepare(cls, values):
        if 'info' in values:
            values.update(values.pop('info'))
            values = [values]
        else:
            values = values['data_items']
        return {'__root__': values}
