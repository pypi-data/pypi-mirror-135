from typing import Optional

from .base import BaseModel


class SearchMeta(BaseModel):
    name: Optional[str]
    description: Optional[str]
    relevance: Optional[float]
