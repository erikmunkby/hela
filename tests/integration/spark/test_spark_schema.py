import pytest
from tests import test_schemas
from catalog.schema_generators import spark_schema
try:
    from pyspark.sql.types import (
        ArrayType, IntegerType, StringType, StructField, StructType, FloatType,
        DateType, TimestampType, LongType
    )
except ModuleNotFoundError:
    pass


@pytest.mark.spark
def test_spark_schema():
    expected_schema = StructType([
        StructField(name='int_col', dataType=IntegerType(), nullable=True),
        StructField(name='string_col', dataType=StringType(), nullable=True),
        StructField(name='date_col', dataType=DateType(), nullable=True),
        StructField(name='datetime_col', dataType=TimestampType(), nullable=True),
        StructField(name='struct_col', dataType=StructType([
            StructField(name='struct_int_col', dataType=IntegerType(), nullable=True),
            StructField(name='struct_float_col', dataType=FloatType(), nullable=True)
        ]), nullable=True),
        StructField(name='array_col', dataType=ArrayType(StringType()), nullable=True),
        StructField(name='sub_cols', dataType=StructType([
            StructField(name='sub_int_col', dataType=IntegerType(), nullable=True),
            StructField(name='sub_long_col', dataType=LongType(), nullable=True)
        ]), nullable=True)
    ])
    assert expected_schema == spark_schema(test_schemas.all_types_no_desc)
