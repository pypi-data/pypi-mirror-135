from datetime import date
from typing import Optional

from pydantic import StrictStr

from .base import BaseModel, Decimal


class SeriesValueEntity(BaseModel):
    value: Optional[Decimal]
    period: date
    periodicity: StrictStr
