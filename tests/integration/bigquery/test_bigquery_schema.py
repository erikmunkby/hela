import pytest
from tests import test_schemas
from catalog.schema_generators import bigquery_schema
try:
    from google.cloud.bigquery import SchemaField
except ModuleNotFoundError:
    pass


@pytest.mark.bigquery
def test_bigquery_schema():
    expected_schema = [
        SchemaField('int_col', 'INT64', 'NULLABLE'),
        SchemaField('string_col', 'STRING', 'NULLABLE'),
        SchemaField('date_col', 'DATE', 'NULLABLE'),
        SchemaField('datetime_col', 'DATETIME', 'NULLABLE'),
        SchemaField('struct_col', 'RECORD', 'NULLABLE', fields=(
            SchemaField('struct_int_col', 'INT64', 'NULLABLE'),
            SchemaField('struct_float_col', 'FLOAT64', 'NULLABLE')
        )),
        SchemaField('array_col', 'STRING', 'REPEATED'),
        SchemaField('sub_cols', 'RECORD', 'NULLABLE', fields=(
            SchemaField('sub_int_col', 'INT64', 'NULLABLE'),
            SchemaField('sub_long_col', 'INT64', 'NULLABLE')
        ))
    ]

    assert expected_schema == bigquery_schema(test_schemas.all_types_no_desc)
