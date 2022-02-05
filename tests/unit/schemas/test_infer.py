import pytest
import pandas as pd
from catalog import Col, NestedCol
from catalog.data_types import Long, String, Date, DateTime, Struct, Double, Array
from catalog.infer import infer_schema_pandas


@pytest.mark.base
def test_pandas_infer(dataframe_with_schema: pd.DataFrame):
    df, schema = dataframe_with_schema
    inferred_schema = infer_schema_pandas(df)

    # The original schema has "subcols" in it, should work with subcols too
    with_subcols_schema = [
        Col('a', Long()),
        Col('b', String()),
        Col('date', Date()),
        Col('time', DateTime()),
        Col('c', Struct({'d': Long(), 'f': Double()})),
        Col('arrays', Array(Long())),
        NestedCol('col_list', [
            Col('x', Long()),
            Col('y', Long())
        ])
    ]
    assert inferred_schema == with_subcols_schema

    # Should work without subcols (column col_list)
    no_subcols_schema = [
        Col('a', Long()),
        Col('b', String()),
        Col('date', Date()),
        Col('time', DateTime()),
        Col('c', Struct({'d': Long(), 'f': Double()})),
        Col('arrays', Array(Long())),
        Col('col_list', Struct({'x': Long(), 'y': Long()}))
    ]
    assert inferred_schema == no_subcols_schema
