from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import Json

from .base import BaseModel


class ObjectModificationRecord(BaseModel):
    user: str
    user_groups: Json = []
    user_type: Literal['ingest', 'API']
    object_id: UUID
    object_type: Literal['series', 'table']
    modification_type: Literal['update', 'create', 'delete']
    modification_date: Optional[datetime]
    upload: Optional[UUID]
