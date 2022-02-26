import pytest
from hela import column_store, Col, NestedCol
from hela.data_types import String


@pytest.mark.base
def test_referencing():
    my_col = Col('my_col', String())

    assert not my_col.from_store

    @column_store()
    class MyStore:
        sub_col = NestedCol('asdf', [my_col])
        a_col = my_col
        same_col = Col('my_col', String())

    assert my_col.from_store
    assert MyStore.a_col == my_col
    assert MyStore.same_col == my_col


@pytest.mark.base
def test_labelling():
    @column_store(label='Base Store')
    class BaseStore:
        test_col = Col('heyo', String())

    assert BaseStore.test_col.label == 'Base Store'
