from typing import Optional, List
from uuid import UUID

from pydantic import StrictStr

from .base import BaseModel


class Bucket(BaseModel):
    id: UUID
    name: str


class SeriesTagEntity(BaseModel):
    name: StrictStr
    buckets: Optional[List[Bucket]]
    value: Optional[StrictStr]
    id: Optional[UUID]
