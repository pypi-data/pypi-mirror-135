from typing import Optional
from uuid import UUID

from pydantic import StrictInt, StrictStr, StrictBool

from .base import BaseModel


class SeriesLineAttributesEntity(BaseModel):
    row_id: UUID
    number: StrictInt
    indent: StrictInt
    label: Optional[StrictStr]
    has_descendants: Optional[StrictBool]

    class Config:
        allow_mutation = True
