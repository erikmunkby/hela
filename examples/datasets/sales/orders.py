from catalog import Col
from catalog.data_types import String, Double
from catalog.datasets.pandas_parquet_dataset import PandasParquetDataset
from examples.column_store import ColumnStore


orders = PandasParquetDataset(
    name='orders',
    description='Collection of orders made by users in the website and in store.',
    rich_description_path='examples/rich_descriptions/orders_dataset.md',
    partition_cols=['date'],
    columns=[
        ColumnStore.user_id,
        ColumnStore.timestamp,
        ColumnStore.date,
        ColumnStore.product_codes,
        ColumnStore.country,
        ColumnStore.store,
        Col('order_id', String(), 'A unique id for each specific order.'),
        Col('order_status', String(), 'The status of the order, e.g. cancelled or completed.'),
        Col('price', Double(), 'How much money the order is worth or customer has to pay.'),
        Col('currency', String(), 'Three letter combination describing currency e.g. EUR.')
    ]
)
