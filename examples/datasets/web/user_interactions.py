from catalog import Col
from catalog.data_types import String
from catalog.datasets.pandas_parquet_dataset import PandasParquetDataset
from examples.column_store import ColumnStore


user_interactions = PandasParquetDataset(
    name='user_interactions',
    description='User interactions related to the web shops, hits gathered as either page view or event style hit.',
    partition_cols=['date'],
    columns=[
        Col('hit_type', String(), 'The type of hit, either page view or event.'),
        Col('hit', String(), 'The name of the hit, when page view this field is null.'),
        ColumnStore.user_id,
        ColumnStore.date,
        Col('session_id', String(), 'A session id binding multiple hits together, timeout of 30 minutes.'),
        Col('page', String(), 'The web page URL path, sent together with every hit.'),
        ColumnStore.timestamp,
        ColumnStore.product_codes,
        ColumnStore.store,
        ColumnStore.country
    ]
)
