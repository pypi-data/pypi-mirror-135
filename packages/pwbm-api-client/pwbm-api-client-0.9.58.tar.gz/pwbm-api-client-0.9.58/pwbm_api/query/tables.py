from copy import deepcopy
from functools import partial
from typing import List, Optional

from pydantic import BaseModel, StrictStr

from pwbm_api.entities import (
    TableQueryEntity,
    SearchByNeumQuery,
    TablesQueryClientEntity,
    TablesDBSorting,
    TablesIndexSorting,
    QueryTypes,
    TablesSortBy,
    TablesSortByDB,
)
from .base import BaseQuery


class TableQuery(BaseQuery):
    api_path = 'explore/tables/'

    endpoint_mapping = {
        'search_tables': '',
        'search_tables_by_neum': 'neum',
        'get_tables': '{table_id}'
    }

    def _determine_endpoint(self):
        if len(self.attributes) > 1:
            raise ValueError
        elif not self.attributes:
            self.endpoint = 'search_tables'
        elif 'search_text' in self.attributes:
            self.endpoint = 'search_tables'
        elif 'neum' in self.attributes:
            self.endpoint = 'search_tables_by_neum'
        elif 'ids' in self.attributes:
            self.endpoint = 'get_tables'
        else:
            raise ValueError('Unable to determine endpoint')

    def filter(
            self,
            sources: Optional[List[StrictStr]] = None,
    ):
        self.attributes.update(
            sources=sources
        )
        return self

    def build(self):
        attributes = deepcopy(self.attributes)
        url_params = {}
        client_filters = {}
        query_type = QueryTypes.table
        if self.endpoint == 'search_tables':
            query = TableQueryEntity(**attributes)
            sorting = TablesIndexSorting
            sort_model = TablesSortBy
        elif self.endpoint == 'search_tables_by_neum':
            query = SearchByNeumQuery(**attributes)
            client_filters = TablesQueryClientEntity(**attributes).dict()
            sorting = TablesDBSorting
            sort_model = TablesSortByDB
        elif self.endpoint == 'get_tables':
            client_filters = TablesQueryClientEntity(**attributes).dict()
            sorting = partial(TablesDBSorting, client_side=True)
            query = BaseModel()
            sort_model = TablesSortByDB
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
