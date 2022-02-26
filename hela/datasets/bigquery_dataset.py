import os
import pandas as pd
from typing import Optional, Sequence
from hela import BaseDataset
from hela._column_classes import _ColumnType
from hela.schema_generators import bigquery_schema
from hela._utils.dict_utils import flatten_dict
try:
    from google.cloud import bigquery
except ModuleNotFoundError:
    pass


class BigqueryDataset(BaseDataset):
    def __init__(
        self,
        name: str,
        database: Optional[str] = None,
        description: Optional[str] = None,
        rich_description_path: Optional[str] = None,
        partition_cols: Optional[Sequence[str]] = None,
        columns: Optional[Sequence[_ColumnType]] = None
    ) -> None:
        super().__init__(
            name,
            data_type='bigquery',
            folder=None,
            database=database,
            description=description,
            rich_description_path=rich_description_path,
            partition_cols=partition_cols,
            columns=columns
        )
        self.client = bigquery.Client()

    @property
    def project_id(self) -> str:
        """Returns the bigquery project id, assumes project_id exists under env variable "CLOUDSDK_CORE_PROJECT"""
        return os.environ['CLOUDSDK_CORE_PROJECT']

    @property
    def table_id(self) -> str:
        """Returns the full table id in style of: "project_id.database_id.table_id"
        Assumes project_id exists under env variable "CLOUDSDK_CORE_PROJECT"
        """
        return f'{self.project_id}.{self.database}.{self.name}'

    def write_json(self, json_rows: Sequence[dict]) -> None:
        self.client.insert_rows_json(self.table_id, json_rows)

    def query_table(self, query_string: str) -> pd.DataFrame:
        """Query this dataset in bigquery. In the FROM part simply write TABLE.
        >>> SELECT * FROM TABLE
        instead of
        >>> SELECT * FROM <some_table_id>

        Args:
            query_string: A query for this dataset/table
        """
        query_string = query_string.replace('FROM TABLE', f'FROM {self.table_id}')

        return self.client.query(query_string).to_dataframe()

    def create_table(self) -> None:
        """Create a bq table given this datasets column schema."""
        table = bigquery.Table(
            self.table_id,
            schema=bigquery_schema(self.columns)
        )
        self.client.create_table(table)

    def create_database(self) -> None:
        """Create a bq database given this datasets database (or its catalog's database)"""
        if self.database is None:
            raise ValueError('Database is None')
        self.client.create_dataset(f'{self.project_id}.{self.database}')

    def delete_table(self) -> None:
        """Delete this table from bigquery"""
        self.client.delete_table(self.table_id)

    def get_samples(self) -> dict:
        df = self.query_table('SELECT * FROM TABLE LIMIT 1')
        sample_dict = df.to_dict(orient='records')[0]
        # Return both original and flattened keys to make sure we have both
        # my_column {a: 1, b: 2}
        # and
        # my_column.a
        # my_column.b
        return {
            **sample_dict,
            **flatten_dict(sample_dict)
        }
