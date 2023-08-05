from typing import List, Union

from pwbm_api import Series, Table
from pwbm_api.entities import SortType, DateRange


class BaseSorting:
    def __init__(self, results: List[Union[Series, Table]], sorting):
        self._results = results
        self._sorting = sorting
        self.sorting_mapping = {}

    def sort_results(self):
        if self._sorting.sort_by:
            sorting = self.sorting_mapping[self._sorting.sort_by]
            sort_key = lambda item: (sorting(item) is None, sorting(item))
            reverse = self._sorting.sort == SortType.descending
            self._results = sorted(self._results, key=sort_key, reverse=reverse)
        return self._results


class SeriesSorting(BaseSorting):
    def __init__(self, results: List[Series], sorting):
        super().__init__(results, sorting)
        self.sorting_mapping = {
            'name': self._by_series_name,
            'uom': self._by_data_type,
            'source': self._by_source_url,
            'start_date': self._by_beginning_date,
            'end_date': self._by_ending_date
        }

    def _by_series_name(self, series: Series):
        return series.name

    def _by_data_type(self, series: Series):
        return series.data_type

    def _by_source_url(self, series: Series):
        return series.source.agency

    def _by_beginning_date(self, series: Series):
        return DateRange.construct_from_string(series.date_range).start_date

    def _by_ending_date(self, series: Series):
        return DateRange.construct_from_string(series.date_range).end_date


class TablesSorting(BaseSorting):
    def __init__(self, results: List[Table], sorting):
        super().__init__(results, sorting)
        self.sorting_mapping = {
            'name': self._by_table_name,
            'source': self._by_source_url
        }

    def _by_table_name(self, table: Table):
        return table.name

    def _by_source_url(self, table: Table):
        return table.source.agency
