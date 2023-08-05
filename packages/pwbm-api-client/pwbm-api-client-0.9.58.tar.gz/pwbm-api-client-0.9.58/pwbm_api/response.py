from copy import deepcopy
from typing import List

import requests
from requests.models import PreparedRequest

from pwbm_api.representations import Series, SeriesItems, TableItems
from .entities import QueryTypes, Paging
from .filters import SeriesFilter, TablesFilter
from .sorting import SeriesSorting, TablesSorting

query_models = {
    QueryTypes.series: SeriesItems,
    QueryTypes.table: TableItems,
}


class Response:
    def __init__(self, query):
        self.query = query
        self.empty = False
        self.initial = True
        self.results = []

    def fetchone(self):
        try:
            item = next(iter(self))
        except StopIteration:
            item = None
        self.empty = True
        self.results = []
        return item

    def fetchall(self):
        items = [item for item in self]
        self.empty = True
        return items

    def __iter__(self):
        if self.initial:
            self._request().filter().sort()
            self.initial = False
        return deepcopy(self)

    def __next__(self):
        if self.empty:
            raise StopIteration
        elif self.query.url_params and not self.results:
            raise StopIteration
        elif self.query.client_filters and not self.results:
            raise StopIteration
        elif not self.results:
            self._update_results_with_paging()
        return self.results.pop(0)

    def _request(self):
        if url_params := self.query.url_params:
            url_params = [dict(zip(url_params, param)) for param in zip(*url_params.values())]
            for params in url_params:
                url = None
                for key, value in params.items():
                    url = self.query.url_template.replace(key, value)
                response = self._make_response(url)
                self._update_results_from_response(response)
        elif self.query.client_filters:
            while True:
                if not self._update_results_with_paging():
                    break
        return self

    def filter(self):
        if self.query.type == QueryTypes.series:
            results_filter = SeriesFilter
        elif self.query.type == QueryTypes.table:
            results_filter = TablesFilter
        else:
            return self
        self.results = results_filter(self.results, self.query.client_filters).filter_results()

        return self

    def sort(self):
        if self.query.sorting.client_side:
            if self.query.type == QueryTypes.series:
                ordering = SeriesSorting
            elif self.query.type == QueryTypes.table:
                ordering = TablesSorting
            else:
                return self
            self.results = ordering(self.results, self.query.sorting).sort_results()
        else:
            return self

    def _make_response(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response

    def _update_results_from_response(self, response):
        json_data = response.json()
        if not self.query.url_params:
            self.query.paging = Paging(**json_data)
        data = query_models[self.query.type](**json_data).__root__
        if not data:
            raise StopIteration

        if self.query.type == QueryTypes.series and data[0].data_items is None:
            data = self._request_series_values(data)

        self.results.extend(data)

    def _request_series_values(self, serieses: List[Series]) -> List[Series]:
        series_ids = [str(series.id) for series in serieses]
        return Response(Series.query(ids=series_ids).build()).fetchall()

    def _update_results_with_paging(self):
        paging = self.query.paging
        url = self.query.url_template
        if paging.page_num and paging.page_num == paging.page_count:
            if self.query.client_filters:
                return None
            raise StopIteration

        req = PreparedRequest()
        req.prepare_url(url, params=paging.dict(by_alias=True, exclude={'page_count'}))
        url = req.url
        self._update_results_from_response(self._make_response(url))

        return self.results
