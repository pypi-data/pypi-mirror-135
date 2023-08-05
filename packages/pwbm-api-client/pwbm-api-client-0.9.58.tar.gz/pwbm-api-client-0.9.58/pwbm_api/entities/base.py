import decimal
import json
from functools import partial
from typing import Optional
from uuid import UUID
import pydantic

from pwbm_api.constants import DECIMAL_INTEGRAL_PLACES, DECIMAL_SCALE
from .date_range import DateRange

# Drop-in replacement for decimal.Decimal type.
# gt and lt limitations are checked only when used in pydantic models.
# For other circumstances decimal context limitations are used.
Decimal = pydantic.condecimal(
    gt=decimal.Decimal(-(10 ** DECIMAL_INTEGRAL_PLACES)),
    lt=decimal.Decimal(+(10 ** DECIMAL_INTEGRAL_PLACES)),
)


def decimal_formatter(value: Optional[Decimal]) -> Decimal:
    """Get string representation of the DataValue. Rounds the value to fit the scale, strips off all trailing zeros."""

    if value is not None:
        if value.to_integral() == value:
            return value.quantize(decimal.Decimal('1'))
        return value.quantize(
            decimal.Decimal(f'0.{"0" * (DECIMAL_SCALE - 1)}{"1" if DECIMAL_SCALE else ""}')
        ).normalize()


class BaseModel(pydantic.BaseModel):
    class Config:
        extra = pydantic.Extra.ignore
        allow_mutation = True
        use_enum_values = True
        json_dumps = partial(json.dumps, sort_keys=True)
        json_encoders = {
            decimal.Decimal: lambda value: str(decimal_formatter(value)),
            DateRange: lambda date_range: str(date_range),
            UUID: lambda value: str(value)
        }
