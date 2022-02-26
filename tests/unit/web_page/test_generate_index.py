from hela.datasets.pandas_parquet_dataset import PandasParquetDataset
from hela import Col, NestedCol, Catalog, generate_webpage
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


def test_generate_index(temp_folder):
    generate_webpage(TestCatalog, str(temp_folder))
