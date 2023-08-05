import re
from copy import deepcopy
from datetime import date
from typing import Tuple

from dateutil.parser import isoparse as parse_datetime


class DateRange:
    _DATE_PATTERN = r'([0-9]{4})(?:-(0?[1-9]|1[0-2])(?:-(0?[1-9]|[12][0-9]|3[01]))?)?'
    _DATE_RANGE_SCHEMA_PATTERN = rf'^({_DATE_PATTERN})?--({_DATE_PATTERN})?$'
    _DATE_RANGE_PATTERN = rf'^(?P<start>{_DATE_PATTERN})?--(?P<end>{_DATE_PATTERN})?$'

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # sort to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # should mutate the dict in place, the returned value will be ignored
        field_schema.update(
            type='string',
            pattern=cls._DATE_RANGE_SCHEMA_PATTERN,
            examples=['--', '1964-01-28--', '1964-01-28--2020-01-01', '--2020-01-01', '1964-01--2020-01-01', '1964-01--2020'],
        )

    @classmethod
    def validate(cls, value):
        if isinstance(value, cls):
            return value
        elif isinstance(value, tuple):
            if value[0] is not None and not isinstance(value[0], date):
                raise TypeError('beginning_date should either None or date')
            if value[1] is not None and not isinstance(value[1], date):
                raise TypeError('beginning_date should either None or date')
            return cls(value)
        elif isinstance(value, str):
            return cls.construct_from_string(value)
        else:
            raise TypeError('string or tuple required')

    @classmethod
    def construct_from_string(cls, s: str):
        if match := re.fullmatch(cls._DATE_RANGE_PATTERN, s):
            if start_date := match.group('start'):
                start_date = parse_datetime(start_date).date()
            if end_date := match.group('end'):
                end_date = parse_datetime(end_date).date()
        else:
            raise ValueError('invalid date range format')
        return cls((start_date, end_date))

    def __init__(self, date_range_tuple: Tuple):
        self.date_range_tuple = date_range_tuple

        self._start_date, self._end_date = self.date_range_tuple
        if self._start_date and self._end_date and self._start_date > self._end_date:
            self._start_date, self._end_date = self._end_date, self._start_date

    @property
    def start_date(self):
        return deepcopy(self._start_date)

    @property
    def end_date(self):
        return deepcopy(self._end_date)

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __repr__(self):
        return f"DateRange('{str(self)}')"

    def __str__(self):
        start_date_str = self._start_date.isoformat() if self._start_date else ''
        end_date_str = self._end_date.isoformat() if self._end_date else ''
        return f"{start_date_str}--{end_date_str}"

    def intersects(self, date_range: 'DateRange') -> bool:
        if date_range.start_date:
            max_start_date = max(self._start_date, date_range.start_date)
        else:
            max_start_date = date_range.start_date

        if date_range.end_date:
            min_end_date = min(self._end_date, date_range.end_date)
        else:
            min_end_date = date_range.end_date

        delta = (min_end_date - max_start_date).days + 1
        overlap = max(0, delta)

        return bool(overlap)
