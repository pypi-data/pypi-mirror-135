from functools import reduce
from typing import List, Optional
from urllib.parse import urlencode, urljoin
from uuid import UUID

from pydantic import StrictStr

from pwbm_api.constants import API_URL
from pwbm_api.entities import SortType, Query


class BaseQuery:
    api_path = None
    endpoint_mapping = {}

    def __init__(
            self,
            search_text: Optional[List[StrictStr]] = None,
            ids: Optional[List[UUID]] = None,
            neum: Optional[StrictStr] = None
    ) -> None:
        self.attributes = {k: v for k, v in dict(search_text=search_text, ids=ids, neum=neum).items() if v is not None}
        self.endpoint = None
        self.client_filter_params = None
        self._determine_endpoint()

    def filter(self):
        raise NotImplemented

    def _determine_endpoint(self):
        raise NotImplemented

    def order_by(self, field: StrictStr, order: Optional[SortType] = SortType.ascending.value):
        if 'sort' in self.attributes or 'sort_by' in self.attributes:
            raise ValueError('"order_by" option already specified.')
        elif not any((field, order)):
            raise ValueError('One of the "sort",  "field" should be specified.')
        elif order not in SortType.__members__.values():
            raise ValueError(f'Invalid sort type "{order}". Valid sort types: {[i.value for i in SortType]}')
        if order:
            self.attributes['sort'] = order
        if field:
            self.attributes['sort_by'] = field

        return self

    def build_url_template(self, attributes):
        url = ''.join(reduce(urljoin, (API_URL, self.api_path, self.endpoint_mapping[self.endpoint])))
        if self.attributes:
            url = f'{url}?{urlencode(attributes)}'
        return url

    def prepare_query(
            self,
            query,
            attributes,
            client_filters,
            sorting,
            sort_model,
            url_params,
            query_type
    ):
        if sort_by := attributes.get('sort_by'):
            try:
                sorting = sorting(**attributes)
            except (ValueError, KeyError):
                raise ValueError(
                    f'Invalid sort field "{sort_by}" for endpoint {self.endpoint}.'
                    f'Valid fields: {[i.value for i in sort_model]}'
                )
        else:
            sorting = sorting(**attributes)

        valid_params = {*query.dict().keys(), *client_filters.keys(), *sorting.dict().keys()}
        if extra_attributes := attributes.keys() - valid_params:
            raise ValueError(f'Query contains extra attributes: {extra_attributes}')
        else:
            sorting_dict = sorting.dict(exclude={'client_side'}, exclude_unset=True) if not sorting.client_side else {}
            query_dict = {'query': query.json(exclude_none=True)} if query.dict() else {}
            attributes = {**query_dict, **sorting_dict}

        return Query(
            url_template=self.build_url_template(attributes),
            url_params=url_params,
            client_filters={k: v for k, v in client_filters.items() if v is not None},
            sorting=sorting,
            type=query_type
        )
