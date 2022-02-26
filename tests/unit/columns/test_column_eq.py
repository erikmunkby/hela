import pytest
from hela.data_types import Double, Int, Struct
from hela import Col, NestedCol


@pytest.mark.base
def test_col_equals():
    c1 = Col('col1', Double())
    c2 = Col('col1', Double())
    c3 = Col('col1', Int())
    c4 = Col('col2', Double())

    assert c1 == c2
    assert c1 != c3
    assert c1 != c4
    assert len({c1, c2, c3, c4}) == 3


@pytest.mark.base
def test_subcol_equals():
    c1 = Col('col1', Double())
    c2 = Col('col1', Double())
    c3 = Col('col1', Int())
    c4 = Col('col2', Double())

    s1 = NestedCol('s1', columns=[c1, c3])
    s2 = NestedCol('s1', columns=[c2, c3])
    s3 = NestedCol('s2', columns=[c1, c3])
    s4 = NestedCol('s1', columns=[c1, c4])

    # Here we are recreating subcol s4 but with Col and Struct, should also be equal
    c5 = Col('s1', data_type=Struct({c1.name: c1.data_type, c4.name: c4.data_type}))

    assert s1 == s2
    assert s1 != s3
    assert s1 != s4
    assert s4 == c5
    assert len({s1, s2, s3, s4}) == 3
