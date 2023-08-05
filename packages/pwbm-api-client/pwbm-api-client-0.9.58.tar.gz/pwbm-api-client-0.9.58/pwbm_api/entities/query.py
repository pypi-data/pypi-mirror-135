from typing import Any, Dict, List, Optional
from enum import Enum

from pydantic import Field

from .base import BaseModel


class QueryTypes(str, Enum):
    series = 'series'
    table = 'table'


class Paging(BaseModel):
    page_size: Optional[int] = 10
    page_count: Optional[int]
    page_num: Optional[int] = Field(..., alias='page')

    class Config(BaseModel.Config):
        allow_population_by_field_name = True


class Query(BaseModel):
    url_template: str
    url_params: Dict[str, List[Any]]
    client_filters: Dict[str, Any]
    sorting: Any
    type: QueryTypes
    paging: Paging = Paging(page_num=0)
