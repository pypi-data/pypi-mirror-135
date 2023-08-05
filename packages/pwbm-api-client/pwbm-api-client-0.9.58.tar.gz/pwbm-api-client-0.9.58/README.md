Python client for PWBM-API

## Requirements
Tool implemented for Python version >= 3.8

## Installation instruction

### Install Python package:
Execute following command:
```shell
pip install pwbm-api-client
```

### Import package and use it
```python

from pwbm_api.client import Client
from pwbm_api import Series, Table
```

### Examples of usage:
```python

from pwbm_api.client import Client
from pwbm_api import Series, Table

client = Client()

# series filtration example
response = client.get(
    Series.query().filter(
        frequencies=['Annual'],
        relates_to_table=True,
        sources=['Internal Revenue Service'],
        tags=[{'name': 'Metric'}],
        uoms=['Items'],
        date_range='2015-12-31--2020-01-01'
    ).order_by(field='name', order='desc')  # permitted field name: 'name', 'uom', 'frequency', 'source', 'start_date', 'end_date'
)

for series in response:
    print(series)

# series search example by multiple search queries
response = client.get(
    Series.query(search_text=['Pennsylvania', 'Business Application']).filter(
        relates_to_table=True,
        sources=['Centers for Disease Control and Prevention'],
        frequencies=['Annual']
    ).filter(
        uoms=['Items'],
        tags=[{'name': 'State'}]
    ).order_by(
        field='name', order='desc'  # permitted field name: 'name', 'uom', 'frequency', 'source', 'start_date', 'end_date'
    )
)

for series in response:
    print(series)

# series search by neum example
response = client.get(
    Series.query(
        neum='Nebraska, Pneumonia and COVID-19 Deaths'
    ).filter(
        sources=['Centers for Disease Control and Prevention'],
        relates_to_table=True
    ).filter(
        frequencies=['Annual'],
        uoms=['People'],
        date_range='2020--2022'
    ).order_by(field='name')
    # permitted field name: 'name', 'uom', 'source', 'start_date', 'end_date', 'row_ver'
)

for series in response:
    print(series)

# get series by ids example
response = client.get(
    Series.query(
        ids=[
            '6cf73546-b8a9-4dbc-978a-4ff91bff8b07',
            'faf42b55-52b3-4ac1-9824-b3126c09ac41',
        ]
    ).filter(
        sources=['CDC'],
        frequencies=['Weekly Ending Sunday'],
        uoms=['People'],
        date_range='2020-01-01--2020-06-01'
    ).order_by(field='name')
    # permitted field name: 'name', 'uom', 'source', 'start_date', 'end_date'
)

for series in response:
    print(series)

# tables filtration example
response = client.get(
    Table.query().filter(
        sources=['Fire Administration']
    ).order_by(field='name')  # permitted field name: 'name', 'source'
)

for table in response:
    print(table)

# tables search example by multiple search queries
response = client.get(
    Table.query(
        search_text=['Other Residential Building']
    ).filter(
        sources=['Fire Administration']
    ).order_by(field='name', order='desc')  # permitted field name: 'name', 'source'
)

for table in response:
    print(table)

# get tables by ids example
response = client.get(
    Table.query(
        ids=['b9746501-aed4-4287-b109-ecb6c6ad39ad', '579b9e3f-cae4-4da0-81c6-234c334e769a']
    ).filter(
        sources=['Fire Administration']
    ).order_by(field='source', order='asc')  # permitted field name: 'name', 'source'
)

for table in response:
    print(table)

# tables search by neum example
response = client.get(
    Table.query(
        neum='Pennsylvania'
    ).filter(
        sources=['Internal Revenue Service']
    ).order_by(field='name', order='desc')  # permitted field name: 'name', 'source', 'row_ver'
)

for table in response:
    print(table)

```