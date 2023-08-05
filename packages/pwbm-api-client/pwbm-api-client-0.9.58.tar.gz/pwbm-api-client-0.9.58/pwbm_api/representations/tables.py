from typing import List, Optional
from uuid import UUID

from pydantic import root_validator, validator

from pwbm_api.entities import BaseModel, SourceEntity
from pwbm_api.entities.table import DataItemInfo
from pwbm_api.query import TableQuery


class Table(BaseModel):
    query = TableQuery

    id: UUID
    name: Optional[str]
    priority: Optional[int]
    description: Optional[str]
    source: Optional[SourceEntity]
    neum: Optional[str]
    data_items: Optional[List[DataItemInfo]]

    @validator('source', pre=True)
    def prepare_source(cls, source):
        if isinstance(source, str):
            source = {'agency': source}
        return source


class TableItems(BaseModel):
    __root__: List[Table]

    @root_validator(pre=True)
    def prepare(cls, values):
        if 'info' in values:
            values.update(values.pop('info'))
            values = [values]
        else:  # search by neum
            values = values['data_items']
        return {'__root__': values}
