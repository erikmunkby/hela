import pytest
import json
from dateutil.parser import parse
from pathlib import Path
from hela.schema_generators import spark_schema
from tests import test_schemas
try:
    from pyspark.sql import SparkSession
except ModuleNotFoundError:
    pass


@pytest.mark.spark
def spark_column_as_list(sdf, column: str) -> list:
    return [x[0] for x in sdf.select(column).collect()]


@pytest.mark.spark
@pytest.fixture(scope='session')
def spark():
    spark = (
        SparkSession.builder
        .appName('testing')
        .master('local[2]')
        .getOrCreate()
    )
    yield spark
    spark.stop()


@pytest.mark.spark
def test_convert_to_spark(spark):
    df = test_schemas.all_types_dataframe.copy()
    df.loc[:, 'date_col'] = df.date_col.apply(lambda x: parse(x).date())
    df.loc[:, 'datetime_col'] = df.datetime_col.apply(lambda x: parse(x))
    schema = spark_schema(test_schemas.all_types_no_desc)
    sdf = spark.createDataFrame(
        df,
        schema=schema
    )

    assert sdf.schema == schema
    df_vals = [x['sub_int_col'] for x in df['sub_cols']]
    sdf_vals = [x[0] for x in sdf.select('sub_cols.sub_int_col').collect()]
    assert df_vals == sdf_vals

    # Cannot accept 123 as struct type, should raise error
    df.loc[:, 'sub_cols'] = 123
    with pytest.raises(TypeError):
        sdf = spark.createDataFrame(df, schema=schema)


@pytest.mark.spark
def test_read_json_spark(spark, temp_path: Path):
    df = test_schemas.all_types_dataframe.copy()
    # Turn into json line object
    df_dict = df.to_dict(orient='records')
    jl = '\n'.join([json.dumps(x) for x in df_dict])

    with open(temp_path, 'w') as f:
        f.write(jl)

    read_schema = spark_schema(test_schemas.all_types_no_desc)
    sdf = spark.read.json(str(temp_path), schema=read_schema)

    assert spark_column_as_list(sdf, 'string_col') == df.string_col.tolist()

    # Remove column and read. Should give back all nulls (None) in that column
    df_dict = df.drop(columns='struct_col').to_dict(orient='records')
    jl = '\n'.join([json.dumps(x) for x in df_dict])

    with open(temp_path, 'w') as f:
        f.write(jl)

    sdf = spark.read.json(str(temp_path), schema=read_schema)

    assert spark_column_as_list(sdf, 'struct_col') == [None for _ in range(len(df))]
