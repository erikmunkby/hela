from catalog import Col, NestedCol
from catalog.data_types import String, Float, Int
from catalog.datasets.pandas_parquet_dataset import PandasParquetDataset
from examples.column_store import ColumnStore


beer_info = PandasParquetDataset(
    name='beer_info',
    description='Meta data for each beer such as description, beer type and alcohol percentage.',
    rich_description_path='examples/rich_descriptions/beer_info.md',
    columns=[
        ColumnStore.product_code,
        ColumnStore.product_name,
        ColumnStore.product_category,
        ColumnStore.country,
        Col('description', String(), 'Description of the beer in terms of flavor and style.'),
        NestedCol('profile', [
            Col('bitterness', Int(), 'Bitterness of the beer on a scale of 1-5.'),
            Col('sourness', Int(), 'Sourness of the beer on a scale of 1-5.')
        ]),
        Col('alcohol_content', Float(), 'Alcohol content in percent.')
    ]
)
