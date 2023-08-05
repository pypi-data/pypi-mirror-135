from functools import partial
from typing import List, Union

from pwbm_api import Series, Table
from pwbm_api.entities import DateRange


class BaseFilter:
    def __init__(self, results: List[Union[Series, Table]], filters):
        self._results = results
        self._filters = filters
        self.filter_mapping = {}

    def filter_results(self):
        for key, filter_option in self._filters.items():
            self._results = list(filter(partial(self.filter_mapping[key], filter_option), self._results))
        return self._results


class SeriesFilter(BaseFilter):
    def __init__(self, results: List[Series], filters):
        super().__init__(results, filters)
        self.filter_mapping = {
            'tags': self._by_tags,
            'sources': self._by_sources,
            'frequencies': self._by_frequencies,
            'uoms': self._by_uoms,
            'relates_to_table': self._by_relates_to_table,
            'date_range': self._by_date_range
        }

    def _by_tags(self, tags, result: Series) -> bool:
        for tag in tags:
            for result_tag in result.tags:
                result_tag = result_tag.dict()
                for key, value in tag.items():
                    if value is not None and result_tag[key] != value:
                        break
                else:
                    break
            else:
                return False
        return True

    def _by_sources(self, sources, result: Series) -> bool:
        return result.source.agency in sources

    def _by_frequencies(self, frequencies, result: Series) -> bool:
        return bool(set(result.periodicity).intersection(set(frequencies)))

    def _by_uoms(self, uoms, result: Series) -> bool:
        return result.data_type in uoms

    def _by_relates_to_table(self, relates_to_table, result: Series) -> bool:
        return bool(result.tables) == relates_to_table

    def _by_date_range(self, date_range: DateRange, result: Series) -> bool:
        result_date_range = DateRange.construct_from_string(result.date_range)
        return date_range.intersects(result_date_range)


class TablesFilter(BaseFilter):
    def __init__(self, results: List[Table], filters):
        super().__init__(results, filters)

        self.filter_mapping = {
            'sources': self._by_sources,
        }

    def _by_sources(self, sources, result: Table) -> bool:
        return result.source.agency in sources
