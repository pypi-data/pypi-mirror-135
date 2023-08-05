from typing import Optional
from uuid import UUID

from pydantic import StrictStr

from .base import BaseModel


class SourceEntity(BaseModel):
    id: Optional[UUID]
    agency: Optional[StrictStr]
    agency_url: Optional[StrictStr]
    source_url: Optional[StrictStr]
