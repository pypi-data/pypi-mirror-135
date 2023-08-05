from copy import deepcopy
from functools import partial
from typing import Dict, List, Optional

from pydantic import BaseModel, StrictBool, StrictStr

from pwbm_api.entities import (
    SeriesQueryEntity,
    SearchByNeumQuery,
    SeriesSortBy,
    SeriesSortByDB,
    SeriesQueryClientEntity,
    SeriesIndexSorting,
    SeriesDBSorting,
    QueryTypes,
)
from .base import BaseQuery


class SeriesQuery(BaseQuery):
    api_path = 'explore/series/'

    endpoint_mapping = {
        'search_series': '',
        'search_series_by_neum': 'neum',
        'get_series': '{series_id}'
    }

    def _determine_endpoint(self):
        if len(self.attributes) > 1:
            raise ValueError
        elif not self.attributes:
            self.endpoint = 'search_series'
        elif 'search_text' in self.attributes:
            self.endpoint = 'search_series'
        elif 'neum' in self.attributes:
            self.endpoint = 'search_series_by_neum'
        elif 'ids' in self.attributes:
            self.endpoint = 'get_series'
        else:
            raise ValueError('Unable to determine endpoint')

    def filter(
            self,
            tags: Optional[List[Dict[StrictStr, StrictStr]]] = None,
            sources: Optional[List[StrictStr]] = None,
            frequencies: Optional[List[StrictStr]] = None,
            uoms: Optional[List[StrictStr]] = None,
            relates_to_table: Optional[StrictBool] = None,
            date_range: Optional[StrictStr] = None
    ):
        self.attributes.update(
            tags=tags,
            sources=sources,
            frequencies=frequencies,
            uoms=uoms,
            relates_to_table=relates_to_table,
            date_range=date_range
        )
        return self

    def build(self):
        query_type = QueryTypes.series
        attributes = deepcopy(self.attributes)
        url_params = {}
        client_filters = {}
        if self.endpoint == 'search_series':
            query = SeriesQueryEntity(**attributes)
            sorting = SeriesIndexSorting
            sort_model = SeriesSortBy
        elif self.endpoint == 'search_series_by_neum':
            query = SearchByNeumQuery(**attributes)
            client_filters = SeriesQueryClientEntity(**attributes).dict()
            sorting = SeriesDBSorting
            sort_model = SeriesSortByDB
        elif self.endpoint == 'get_series':
            client_filters = SeriesQueryClientEntity(**attributes).dict()
            sorting = partial(SeriesDBSorting, client_side=True)
            query = BaseModel()
            sort_model = SeriesSortByDB
            url_params[self.endpoint_mapping[self.endpoint]] = attributes.pop('ids')
        else:
            raise ValueError()

        return self.prepare_query(
            query,
            attributes,
            client_filters,
            sorting,
            sort_model,
            url_params,
            query_type
        )
