from typing import Optional

from pydantic import StrictStr

from .base import BaseModel


class TagEntity(BaseModel):
    name: StrictStr
    value: Optional[StrictStr]
