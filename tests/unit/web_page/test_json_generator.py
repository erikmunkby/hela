import json
import pytest
from hela.web_page._json_generator import JsonGenerator
from hela.datasets.pandas_parquet_dataset import PandasParquetDataset
from hela import Col, NestedCol, Catalog
from hela.data_types import Int, String

test_dataset = PandasParquetDataset(
    name='test_dataset',
    description='Test Dataset Structure.',
    columns=[
        Col('test_col', Int(), 'testcol'),
        NestedCol('nested', [
            Col('test_col2', String(), 'nested testcol'),
            Col('filler_col', String(), 'filler col')
        ])
    ]
)
test_dataset._id = 'test_id'


@Catalog.setup(description='Test Catalog Structure.')
class TestCatalog(Catalog):
    test_dataset = test_dataset


@pytest.mark.base
def test_json_generator():
    excepted_output = [
        {'name': 'TestCatalog',
         'type': 'Catalog',
         'description': 'Test Catalog Structure.',
         'rich_description': None,
         'id': 'TestCatalog',
         'children': [
             {'name': 'test_dataset',
              'type': 'Dataset',
              'description': 'Test Dataset Structure.',
              'rich_description': None,
              'id': 'test_id',
              'columns': [
                  {'name': 'test_col',
                   'data_type': 'Int',
                   'description': 'testcol',
                   'from_store': False,
                   'sample_data': None,
                   'other_dataset': []
                   },
                  {'name': 'nested.test_col2',
                   'data_type': 'String',
                   'description': 'nested testcol',
                   'from_store': False,
                   'sample_data': None,
                   'other_dataset': []
                   },
                  {'name': 'nested.filler_col',
                   'data_type': 'String',
                   'description': 'filler col',
                   'from_store': False,
                   'sample_data': None,
                   'other_dataset': []
                   }
              ]
              }]
         }
    ]
    jg = JsonGenerator()
    assert json.loads(jg.generate_docs_jsons([TestCatalog], include_samples=False)) == excepted_output
