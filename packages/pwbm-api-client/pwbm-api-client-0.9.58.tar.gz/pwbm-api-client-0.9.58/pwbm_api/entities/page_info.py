from enum import Enum

from .base import BaseModel


class PageInfoEntity(BaseModel):
    page_size: int
    page_count: int
    page_num: int


class DescendantsHierarchyOptions(str, Enum):
    all = "all"
    direct = "direct"


class DescendantsOptions(str, Enum):
    all = "all"
    direct = "direct"
    find_within_table = "find_within_table"
