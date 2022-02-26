import pytest
from hela.errors import ValidationError
from hela.test_suite import column_store_tests
from hela import column_store, Col
from hela.data_types import String, Bool


@pytest.mark.base
def test_column_duplications():
    @column_store()
    class MyStore:
        a = Col('a', String())
        b = Col('b', String())
        c = Col('b', Bool())

    assert column_store_tests.validate_no_duplicate_columns(MyStore)

    @column_store()
    class MyStore:
        a = Col('a', String())
        b = Col('b', String())
        c = Col('b', String())

    with pytest.raises(ValidationError):
        column_store_tests.validate_no_duplicate_columns(MyStore)


@pytest.mark.base
def test_column_field_names():
    @column_store()
    class MyStore:
        a = Col('a', String())
        b = Col('b', String())

    assert column_store_tests.validate_column_store_field_names(MyStore)

    @column_store()
    class MyStore:
        a = Col('a', String())
        c = Col('b', String())

    with pytest.raises(ValidationError):
        column_store_tests.validate_column_store_field_names(MyStore)
