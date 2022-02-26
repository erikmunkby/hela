"""Module used to translate from catalog schema to other schema types."""
from hela._column_classes import _ColumnType
from hela import BaseDataset
from typing import Sequence, Union


def _get_columns(obj: Union[Sequence[_ColumnType], BaseDataset]) -> Sequence[_ColumnType]:
    if isinstance(obj, BaseDataset):
        obj = obj.columns
    if len(obj) == 0:
        raise ValueError('The column list is empty.')
    return obj


def spark_schema(obj: Union[Sequence[_ColumnType], BaseDataset]):
    col_list = _get_columns(obj)
    from pyspark.sql.types import StructType
    return StructType([c._spark_type() for c in col_list])


def aws_glue_schema(obj: Union[Sequence[_ColumnType], BaseDataset]):
    col_list = _get_columns(obj)
    return [c._glue_type() for c in col_list]


def bigquery_schema(obj: Union[Sequence[_ColumnType], BaseDataset]):
    col_list = _get_columns(obj)
    return [c._bigquery_type() for c in col_list]


def json_schema(obj: Union[Sequence[_ColumnType], BaseDataset]):
    col_list = _get_columns(obj)
    properties = {}
    for c in col_list:
        properties.update(c._json_type())
    return {
        '$schema': 'http://json-schema.org/draft-07/schema',
        'type': 'object',
        'properties': properties
    }
