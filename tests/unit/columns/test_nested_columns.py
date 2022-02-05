import pytest
from catalog.data_types import String, Bool, Struct, Int
from catalog import Col


@pytest.mark.base
def test_build_nested():
    [
        Col('str_col', data_type=String()),
        Col('bool_col', data_type=Bool()),
        Col('struct_col', data_type=Struct({'a': Int(), 'b': String()}))
    ]
